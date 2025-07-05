import os
import json
import time
from functools import wraps
from flask import Blueprint, redirect, url_for, session, request, flash, current_app, render_template, jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from app.models.pending_video import PendingVideo
from app.models.user import User
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets
import logging

# Allow insecure transport for development (HTTP instead of HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

youtube_bp = Blueprint('youtube', __name__)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

# Client configuration - move to environment variables in production
CLIENT_CONFIG = {
    "web": {
        "client_id": "15177856373-sl0cm3l80bncbsov7551ptm6jr40qmru.apps.googleusercontent.com",
        "project_id": "trusty-coder-462513-h6", 
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://127.0.0.1:5000/youtube/oauth2callback",
            "http://localhost:5000/youtube/oauth2callback"
        ]
    }
}

ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}
MAX_FILE_SIZE = 128 * 1024 * 1024 * 1024  # 128GB

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def validate_file_size(file):
    """Validate file size before processing."""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

def login_required(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this feature.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def creator_required(f):
    """Decorator to require creator role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'creator':
            flash("Creator access required.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def youtube_connected_required(f):
    """Decorator to require YouTube connection."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.youtube_connected:
            flash("Connect your YouTube account first.", "warning")
            return redirect(url_for('views.creator_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_youtube_service(user_id=None):
    """Build YouTube API service with user-specific credentials."""
    if user_id is None:
        user_id = session.get('user_id')
    
    if not user_id:
        return None
    
    user = User.query.get(user_id)
    if not user or not user.youtube_connected:
        return None
    
    try:
        credentials_dict = user.get_youtube_credentials()
        if not credentials_dict:
            return None
            
        credentials = Credentials(**credentials_dict)
        
        # Check if credentials need refresh
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Update stored credentials
            user.set_youtube_credentials({
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            })
            db.session.commit()
        
        return build('youtube', 'v3', credentials=credentials, cache_discovery=False)
    except Exception as e:
        logger.error(f"Failed to build YouTube service for user {user_id}: {e}")
        return None

@youtube_bp.route('/authorize')
@login_required
def authorize():
    """Initialize OAuth2 flow for YouTube authorization."""
    try:
        flow = Flow.from_client_config(CLIENT_CONFIG, SCOPES)
        flow.redirect_uri = url_for('youtube.oauth2callback', _external=True)
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        session['state'] = state
        return redirect(authorization_url)
        
    except Exception as e:
        logger.error(f"YouTube authorization error: {e}")
        flash("Unable to connect to YouTube. Please try again.", "error")
        return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/oauth2callback')
@login_required
def oauth2callback():
    """Handle OAuth2 callback from Google."""
    try:
        state = session.get('state')
        
        flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, state=state)
        flow.redirect_uri = url_for('youtube.oauth2callback', _external=True)
        
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Get current user
        user = User.query.get(session['user_id'])
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('auth.login'))
        
        # Store credentials in database for this specific user
        user.set_youtube_credentials({
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        })
        
        # Get channel information
        youtube = build('youtube', 'v3', credentials=credentials, cache_discovery=False)
        response = youtube.channels().list(part='snippet', mine=True).execute()
        
        if response.get('items'):
            channel = response['items'][0]
            user.youtube_channel_name = channel['snippet']['title']
            flash(f"Successfully connected to YouTube channel: {channel['snippet']['title']}", "success")
        else:
            flash("No YouTube channel found for this account.", "warning")
        
        # Save user changes to database
        db.session.commit()
        
        # Redirect based on user role
        if user.role == 'editor':
            return redirect(url_for('views.editor_dashboard'))
        else:
            return redirect(url_for('views.creator_dashboard'))
        
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        flash("Authentication failed. Please try again.", "error")
    
    # Default redirect based on user role
    user = User.query.get(session.get('user_id'))
    if user and user.role == 'editor':
        return redirect(url_for('views.editor_dashboard'))
    else:
        return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/disconnect')
@login_required
def disconnect():
    """Disconnect YouTube account."""
    try:
        user = User.query.get(session['user_id'])
        if user:
            user.disconnect_youtube()
            db.session.commit()
            flash("YouTube account disconnected successfully.", "success")
        else:
            flash("User not found.", "error")
    except Exception as e:
        logger.error(f"Disconnect error: {e}")
        flash("Error disconnecting YouTube account.", "error")
    
    return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/upload-video')
@login_required
def upload_video():
    """Display video upload form."""
    # Get current user
    user = User.query.get(session['user_id'])
    if not user or user.role != 'editor':
        flash("Editor access required.", "danger")
        return redirect(url_for('auth.login'))
    
    # Get creators who have accepted invitations from this editor
    from app.models.invitation import Invitation
    accepted_invitations = Invitation.query.filter_by(
        editor_id=user.id,
        status='accepted'
    ).all()
    
    # Get the creator objects
    available_creators = [inv.creator for inv in accepted_invitations]
    
    return render_template('upload_video.html', available_creators=available_creators)

@youtube_bp.route('/upload', methods=['POST'])
@login_required
def upload_process():
    """Process video upload and create pending video record."""
    try:
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags = request.form.get('tags', '').strip()
        privacy = request.form.get('privacy', 'private').strip()
        creator_id = request.form.get('creator_id')
        
        # Validate required fields
        if not title:
            flash("Video title is required.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        if not creator_id:
            flash("Please select a creator.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        # Validate that the editor has an accepted invitation from this creator
        user = User.query.get(session['user_id'])
        if user.role == 'editor':
            from app.models.invitation import Invitation
            invitation = Invitation.query.filter_by(
                editor_id=user.id,
                creator_id=creator_id,
                status='accepted'
            ).first()
            
            if not invitation:
                flash("You don't have permission to upload videos for this creator.", "error")
                return redirect(url_for('youtube.upload_video'))
        
        # Validate file
        if 'video_file' not in request.files:
            flash("No video file selected.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        video_file = request.files['video_file']
        
        if video_file.filename == '':
            flash("No video file selected.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        if not allowed_file(video_file.filename):
            flash("Invalid file type. Please upload a valid video file.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        if not validate_file_size(video_file):
            flash("File size too large. Maximum size is 128GB.", "error")
            return redirect(url_for('youtube.upload_video'))
        
        # Validate privacy setting
        valid_privacy_settings = ['public', 'unlisted', 'private']
        if privacy not in valid_privacy_settings:
            privacy = 'private'  # Default to private if invalid setting
        
        # Create upload directory
        upload_dir = 'pending_uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with timestamp
        filename = secure_filename(video_file.filename)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_dir, filename)
        
        video_file.save(filepath)
        
        # Create database record
        new_video = PendingVideo(
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy,
            filename=filename,
            filepath=filepath,
            uploader_id=session['user_id'],
            creator_id=creator_id,
            status='pending'
        )
        
        db.session.add(new_video)
        db.session.commit()
        
        flash('Video uploaded successfully and sent for approval.', 'success')
        logger.info(f"Video uploaded: {title} by user {session['user_id']}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Upload error: {e}")
        flash("An error occurred while uploading your video. Please try again.", "error")
    
    return redirect(url_for('views.editor_dashboard'))

@youtube_bp.route('/approve/<int:video_id>')
@login_required
@creator_required
def approve_video(video_id):
    """Approve a pending video and upload to YouTube."""
    try:
        video = PendingVideo.query.get_or_404(video_id)
        
        if video.status != 'pending':
            flash("Video is not pending approval.", "warning")
            return redirect(url_for('views.creator_dashboard'))
        
        # Check if user is the assigned creator
        if video.creator_id != session['user_id']:
            flash("You can only approve videos assigned to you.", "error")
            return redirect(url_for('views.creator_dashboard'))

        # Check if user has YouTube credentials in database
        user = User.query.get(session['user_id'])
        if not user or not user.youtube_connected:
            flash("Please connect your YouTube account first.", "warning")
            return redirect(url_for('youtube.authorize'))

        # Attempt to upload to YouTube
        upload_success = upload_video_to_youtube(video)
        
        if upload_success:
            video.status = 'approved'
            video.youtube_video_id = upload_success  # Store YouTube video ID
            video.updated_at = datetime.now()
            db.session.commit()
            
            flash(f"Video '{video.title}' approved and uploaded to YouTube successfully!", "success")
            logger.info(f"Video approved and uploaded: {video.title} (ID: {video_id})")
        else:
            flash(f"Video '{video.title}' approved but YouTube upload failed. Please try again.", "warning")
            video.status = 'approved'
            video.updated_at = datetime.now()
            db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Approval error: {e}")
        flash("Error approving video.", "error")
    
    return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/reject/<int:video_id>', methods=['GET', 'POST'])
@login_required
@creator_required
def reject_video(video_id):
    """Reject a pending video."""
    try:
        video = PendingVideo.query.get_or_404(video_id)
        
        if video.status != 'pending':
            flash("Video is not pending approval.", "warning")
            return redirect(url_for('views.creator_dashboard'))
        
        # Check if user is the assigned creator
        if video.creator_id != session['user_id']:
            flash("You can only reject videos assigned to you.", "error")
            return redirect(url_for('views.creator_dashboard'))
        
        video.status = 'rejected'
        video.updated_at = datetime.now()
        
        # Add rejection reason if provided
        if request.method == 'POST':
            video.review_notes = request.form.get('reason', '')
        
        db.session.commit()
        
        # Clean up file
        try:
            if video.filepath and os.path.exists(video.filepath):
                os.remove(video.filepath)
        except Exception as cleanup_error:
            logger.warning(f"Failed to cleanup rejected video file: {cleanup_error}")
        
        flash(f"Video '{video.title}' rejected.", "info")
        logger.info(f"Video rejected: {video.title} (ID: {video_id})")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Rejection error: {e}")
        flash("Error rejecting video.", "error")
    
    return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/channel-settings')
@login_required
@youtube_connected_required
def channel_settings():
    """Display YouTube channel settings."""
    try:
        youtube = get_youtube_service()
        if not youtube:
            flash("Unable to connect to YouTube. Please reconnect your account.", "error")
            return redirect(url_for('views.creator_dashboard'))
        
        response = youtube.channels().list(part='snippet,statistics', mine=True).execute()
        
        if not response.get('items'):
            flash("No channel information found.", "warning")
            return redirect(url_for('views.creator_dashboard'))
        
        return render_template('channel_settings.html', channel_info=response['items'][0])
        
    except HttpError as e:
        logger.error(f"YouTube API error: {e}")
        flash("Error loading channel settings. Please try again.", "error")
        return redirect(url_for('views.creator_dashboard'))
    except Exception as e:
        logger.error(f"Channel settings error: {e}")
        flash("An unexpected error occurred.", "error")
        return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/status/<int:video_id>')
@login_required
def video_status(video_id):
    """Get video status information."""
    try:
        video = PendingVideo.query.get_or_404(video_id)
        
        # Check if user owns this video or has creator privileges
        user = User.query.get(session['user_id'])
        if not (video.uploader_id == session['user_id'] or 
                (user.role == 'creator' and video.creator_id == session['user_id'])):
            flash("Access denied.", "error")
            return redirect(url_for('views.creator_dashboard'))
        
        return render_template('video_status.html', video=video)
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        flash("Error retrieving video status.", "error")
        return redirect(url_for('views.creator_dashboard'))

# API Routes for AJAX calls
@youtube_bp.route('/api/youtube-status')
@login_required
def api_youtube_status():
    """API endpoint to check YouTube connection status."""
    try:
        connected = 'credentials' in session
        channel_name = session.get('youtube_channel_name', '')
        
        return {
            'connected': connected,
            'channel_name': channel_name
        }
    except Exception as e:
        logger.error(f"API status error: {e}")
        return {'connected': False, 'channel_name': ''}

@youtube_bp.route('/api/notifications/count')
@login_required
def api_notifications_count():
    """API endpoint to get notification counts."""
    try:
        user = User.query.get(session['user_id'])
        if user.role == 'creator':
            pending_count = PendingVideo.query.filter_by(
                creator_id=session['user_id'], 
                status='pending'
            ).count()
        else:
            pending_count = 0
        
        return {'pending': pending_count}
    except Exception as e:
        logger.error(f"API notifications error: {e}")
        return {'pending': 0}

# YouTube API endpoints
@youtube_bp.route('/api/youtube/status')
@login_required
def youtube_status():
    """API endpoint to check YouTube connection status."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'connected': False, 'channel_name': ''}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'connected': False, 'channel_name': ''}), 404
        
        response = jsonify({
            'connected': user.youtube_connected,
            'channel_name': user.youtube_channel_name or '',
            'timestamp': int(time.time())  # Add timestamp to prevent caching
        })
        
        # Add cache-busting headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    except Exception as e:
        logger.error(f"YouTube status check error: {e}")
        return jsonify({'connected': False, 'channel_name': ''}), 500

# Error handlers
@youtube_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors in YouTube blueprint."""
    flash("The requested resource was not found.", "error")
    return redirect(url_for('views.creator_dashboard'))

@youtube_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors in YouTube blueprint."""
    db.session.rollback()
    logger.error(f"Internal error in YouTube blueprint: {error}")
    flash("An internal error occurred. Please try again.", "error")
    return redirect(url_for('views.creator_dashboard'))

@youtube_bp.route('/debug-session')
@login_required
def debug_session():
    """Debug endpoint to check session contents"""
    session_data = {
        'user_id': session.get('user_id'),
        'credentials': 'credentials' in session,
        'youtube_channel_name': session.get('youtube_channel_name'),
        'all_session_keys': list(session.keys())
    }
    return session_data

def upload_video_to_youtube(video):
    """Upload a video to YouTube and return the video ID if successful."""
    try:
        # Get the creator's credentials from the database
        creator = User.query.get(video.creator_id)
        if not creator or not creator.youtube_connected:
            logger.error(f"Creator {video.creator_id} not found or not connected to YouTube")
            return False
        
        creds_dict = creator.get_youtube_credentials()
        if not creds_dict:
            logger.error(f"No YouTube credentials found for creator {video.creator_id}")
            return False
        
        credentials = Credentials(
            token=creds_dict['token'],
            refresh_token=creds_dict['refresh_token'],
            token_uri=creds_dict['token_uri'],
            client_id=creds_dict['client_id'],
            client_secret=creds_dict['client_secret'],
            scopes=creds_dict['scopes']
        )
        
        # Check if credentials need refresh
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Update stored credentials
            creator.set_youtube_credentials({
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            })
            db.session.commit()
        
        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=credentials, cache_discovery=False)
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': video.title,
                'description': video.description or '',
                'tags': video.tags.split(',') if video.tags else [],
                'categoryId': '22'  # People & Blogs category
            },
            'status': {
                'privacyStatus': video.privacy_status or 'private'  # Use the privacy setting from the video
            }
        }
        
        # Get the video file path
        video_file_path = os.path.join('pending_uploads', video.filename)
        
        if not os.path.exists(video_file_path):
            logger.error(f"Video file not found: {video_file_path}")
            return False
        
        # Create media upload object
        media = MediaFileUpload(
            video_file_path,
            mimetype='video/*',
            resumable=True,
            chunksize=1024*1024  # 1MB chunks
        )
        
        # Upload the video
        logger.info(f"Starting YouTube upload for: {video.title}")
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Upload progress: {int(status.progress() * 100)}%")
        
        if 'id' in response:
            youtube_video_id = response['id']
            logger.info(f"Video uploaded successfully to YouTube: {youtube_video_id}")
            return youtube_video_id
        else:
            logger.error(f"YouTube upload failed: {response}")
            return False
            
    except HttpError as e:
        logger.error(f"YouTube API error: {e}")
        return False
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return False