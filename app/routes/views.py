from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models.user import User
from app.models.pending_video import PendingVideo
from app.models.invitation import Invitation
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func
import json

views = Blueprint('views', __name__)

# Creator Dashboard - sees videos pending their approval or uploaded by them
@views.route('/creator')
def creator_dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Check if user has creator role
    if user.role != 'creator':
        flash("Access denied. Creator access required.", "danger")
        return redirect(url_for('auth.login'))

    # Fetch pending videos where the user is the assigned creator
    pending_videos = PendingVideo.query.filter_by(creator_id=user.id, status='pending').all()

    # Get additional stats
    total_videos = PendingVideo.query.filter_by(creator_id=user.id).count()
    approved_videos_count = PendingVideo.query.filter_by(creator_id=user.id, status='approved').count()
    
    # Get recent approved videos (last 5)
    approved_videos = PendingVideo.query.filter_by(creator_id=user.id, status='approved').order_by(PendingVideo.updated_at.desc()).limit(5).all()
    
    # Get team members (editors who have accepted invitations from this creator)
    from app.models.invitation import Invitation
    accepted_invitations = Invitation.query.filter_by(
        creator_id=user.id,
        status='accepted'
    ).all()
    
    # Count all editors with accepted invitations (editors don't need YouTube connections)
    team_members = len(accepted_invitations)

    # Get current date
    current_date = datetime.now()

    # YouTube connection status - use user's database record
    youtube_connected = user.youtube_connected
    youtube_channel_name = user.youtube_channel_name or ''

    return render_template('creator_dashboard.html', 
                         user=user, 
                         pending_videos=pending_videos,
                         approved_videos=approved_videos,
                         total_videos=total_videos,
                         approved_videos_count=approved_videos_count,
                         team_members=team_members,
                         current_date=current_date,
                         youtube_connected=youtube_connected,
                         youtube_channel_name=youtube_channel_name)


# Editor Dashboard - manages YouTube uploads
@views.route('/editor')
def editor_dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Check if user has editor role
    if user.role != 'editor':
        flash("Access denied. Editor access required.", "danger")
        return redirect(url_for('auth.login'))

    # Get editor's video statistics
    total_uploads = PendingVideo.query.filter_by(uploader_id=user.id).count()
    pending_count = PendingVideo.query.filter_by(uploader_id=user.id, status='pending').count()
    approved_count = PendingVideo.query.filter_by(uploader_id=user.id, status='approved').count()
    
    # Get recent videos (last 5)
    recent_videos = PendingVideo.query.filter_by(uploader_id=user.id).order_by(PendingVideo.created_at.desc()).limit(5).all()
    
    # Get approved videos with YouTube links (last 10)
    approved_videos = PendingVideo.query.filter_by(uploader_id=user.id, status='approved').order_by(PendingVideo.updated_at.desc()).limit(10).all()

    # Get pending invitations for this editor
    pending_invitations = Invitation.query.filter_by(editor_id=user.id, status='pending').all()

    # Get current date
    current_date = datetime.now()

    return render_template('editor_dashboard.html', 
                         user=user, 
                         current_date=current_date,
                         total_uploads=total_uploads,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         recent_videos=recent_videos,
                         approved_videos=approved_videos,
                         pending_invitations=pending_invitations)

@views.route('/search-editors', methods=['GET'])
def search_editors():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Only creators can search for editors
    if user.role != 'creator':
        flash("Access denied. Creator access required.", "danger")
        return redirect(url_for('auth.login'))

    query = request.args.get('query', '').strip()
    if not query:
        return redirect(url_for('views.invite_editor'))

    # Search only users with 'editor' role
    results = User.query.filter(
        User.role == 'editor',
        (User.name.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
    ).all()

    return render_template('invite_editor.html', 
                         user=user, 
                         search_results=results)


@views.route('/send-invite/<int:editor_id>', methods=['POST'])
def send_invitation(editor_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))

    creator = User.query.get(session['user_id'])
    if not creator:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Only creators can send invitations
    if creator.role != 'creator':
        flash("Access denied. Creator access required.", "danger")
        return redirect(url_for('auth.login'))

    editor = User.query.get_or_404(editor_id)

    # Check if invitation already exists
    existing_invitation = Invitation.query.filter_by(
        creator_id=creator.id,
        editor_id=editor.id
    ).first()

    if existing_invitation:
        if existing_invitation.status == 'pending':
            flash(f"Invitation already sent to {editor.name}.", "info")
        elif existing_invitation.status == 'accepted':
            flash(f"{editor.name} has already accepted your invitation.", "info")
        else:
            # Update existing declined invitation to pending
            existing_invitation.status = 'pending'
            existing_invitation.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f"Invitation re-sent to {editor.name}!", "success")
    else:
        # Create new invitation
        invitation = Invitation(
            creator_id=creator.id,
            editor_id=editor.id,
            status='pending'
        )
        db.session.add(invitation)
        db.session.commit()
        flash(f"Invitation sent to {editor.name}!", "success")

    return redirect(url_for('views.invite_editor'))

@views.route('/invite-editor')
def invite_editor():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Check if user has creator role
    if user.role != 'creator':
        flash("Access denied. Creator access required.", "danger")
        return redirect(url_for('auth.login'))

    return render_template('invite_editor.html', user=user)

# Invitation handling routes
@views.route('/accept-invitation/<int:invitation_id>', methods=['POST'])
def accept_invitation(invitation_id):
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user or user.role != 'editor':
        flash("Access denied.", "danger")
        return redirect(url_for('auth.login'))

    invitation = Invitation.query.get_or_404(invitation_id)
    
    # Check if the invitation is for this editor
    if invitation.editor_id != user.id:
        flash("You are not authorized to accept this invitation.", "danger")
        return redirect(url_for('views.editor_dashboard'))

    # Check if invitation is still pending
    if invitation.status != 'pending':
        flash("This invitation has already been processed.", "warning")
        return redirect(url_for('views.editor_dashboard'))

    # Accept the invitation
    invitation.status = 'accepted'
    invitation.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f"Successfully accepted invitation from {invitation.creator.name}!", "success")
    return redirect(url_for('views.editor_dashboard'))

@views.route('/decline-invitation/<int:invitation_id>', methods=['POST'])
def decline_invitation(invitation_id):
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user or user.role != 'editor':
        flash("Access denied.", "danger")
        return redirect(url_for('auth.login'))

    invitation = Invitation.query.get_or_404(invitation_id)
    
    # Check if the invitation is for this editor
    if invitation.editor_id != user.id:
        flash("You are not authorized to decline this invitation.", "danger")
        return redirect(url_for('views.editor_dashboard'))

    # Check if invitation is still pending
    if invitation.status != 'pending':
        flash("This invitation has already been processed.", "warning")
        return redirect(url_for('views.editor_dashboard'))

    # Decline the invitation
    invitation.status = 'declined'
    invitation.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f"Declined invitation from {invitation.creator.name}.", "info")
    return redirect(url_for('views.editor_dashboard'))

@views.route('/analytics')
def analytics():
    """Analytics dashboard for creators and editors"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Get analytics data based on user role
    if user.role == 'creator':
        # Creator analytics
        total_videos = PendingVideo.query.filter_by(creator_id=user.id).count()
        approved_videos = PendingVideo.query.filter_by(creator_id=user.id, status='approved').count()
        pending_videos = PendingVideo.query.filter_by(creator_id=user.id, status='pending').count()
        rejected_videos = PendingVideo.query.filter_by(creator_id=user.id, status='rejected').count()
        
        # Team members count
        accepted_invitations = Invitation.query.filter_by(creator_id=user.id, status='accepted').count()
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_uploads = PendingVideo.query.filter(
            PendingVideo.creator_id == user.id,
            PendingVideo.created_at >= thirty_days_ago
        ).count()
        
        # Weekly activity for chart
        weekly_data = []
        for i in range(7):
            week_start = datetime.now() - timedelta(days=(i+1)*7)
            week_end = datetime.now() - timedelta(days=i*7)
            week_uploads = PendingVideo.query.filter(
                PendingVideo.creator_id == user.id,
                PendingVideo.created_at >= week_start,
                PendingVideo.created_at < week_end
            ).count()
            weekly_data.append({
                'week': f"Week {i+1}",
                'uploads': week_uploads
            })
        weekly_data.reverse()
        
        analytics_data = {
            'total_videos': total_videos,
            'approved_videos': approved_videos,
            'pending_videos': pending_videos,
            'rejected_videos': rejected_videos,
            'team_members': accepted_invitations,
            'recent_uploads': recent_uploads,
            'weekly_data': weekly_data,
            'approval_rate': round((approved_videos / total_videos * 100) if total_videos > 0 else 0, 1)
        }
        
    else:  # Editor analytics
        total_uploads = PendingVideo.query.filter_by(uploader_id=user.id).count()
        approved_uploads = PendingVideo.query.filter_by(uploader_id=user.id, status='approved').count()
        pending_uploads = PendingVideo.query.filter_by(uploader_id=user.id, status='pending').count()
        rejected_uploads = PendingVideo.query.filter_by(uploader_id=user.id, status='rejected').count()
        
        # Recent activity
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_uploads = PendingVideo.query.filter(
            PendingVideo.uploader_id == user.id,
            PendingVideo.created_at >= thirty_days_ago
        ).count()
        
        # Weekly upload data
        weekly_data = []
        for i in range(7):
            week_start = datetime.now() - timedelta(days=(i+1)*7)
            week_end = datetime.now() - timedelta(days=i*7)
            week_uploads = PendingVideo.query.filter(
                PendingVideo.uploader_id == user.id,
                PendingVideo.created_at >= week_start,
                PendingVideo.created_at < week_end
            ).count()
            weekly_data.append({
                'week': f"Week {i+1}",
                'uploads': week_uploads
            })
        weekly_data.reverse()
        
        analytics_data = {
            'total_uploads': total_uploads,
            'approved_uploads': approved_uploads,
            'pending_uploads': pending_uploads,
            'rejected_uploads': rejected_uploads,
            'recent_uploads': recent_uploads,
            'weekly_data': weekly_data,
            'approval_rate': round((approved_uploads / total_uploads * 100) if total_uploads > 0 else 0, 1)
        }

    return render_template('analytics.html', user=user, analytics=analytics_data)

@views.route('/settings')
def settings():
    """User settings page"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    return render_template('settings.html', user=user)

@views.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Get user statistics
    if user.role == 'creator':
        stats = {
            'total_videos': PendingVideo.query.filter_by(creator_id=user.id).count(),
            'approved_videos': PendingVideo.query.filter_by(creator_id=user.id, status='approved').count(),
            'team_members': Invitation.query.filter_by(creator_id=user.id, status='accepted').count()
        }
    else:
        stats = {
            'total_uploads': PendingVideo.query.filter_by(uploader_id=user.id).count(),
            'approved_uploads': PendingVideo.query.filter_by(uploader_id=user.id, status='approved').count(),
            'active_creators': Invitation.query.filter_by(editor_id=user.id, status='accepted').count()
        }

    return render_template('profile.html', user=user, stats=stats)

@views.route('/update-profile', methods=['POST'])
def update_profile():
    """Update user profile"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Update user information
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    
    if not name:
        flash("Name is required.", "danger")
        return redirect(url_for('views.profile'))
    
    if not email:
        flash("Email is required.", "danger")
        return redirect(url_for('views.profile'))
    
    # Check if email is already taken by another user
    existing_user = User.query.filter(User.email == email, User.id != user.id).first()
    if existing_user:
        flash("Email is already taken by another user.", "danger")
        return redirect(url_for('views.profile'))
    
    user.name = name
    user.email = email
    db.session.commit()
    
    flash("Profile updated successfully!", "success")
    return redirect(url_for('views.profile'))

@views.route('/my-videos')
def my_videos():
    """Display user's video uploads"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Get user's videos based on role
    if user.role == 'creator':
        # Creators see all videos assigned to them
        videos = PendingVideo.query.filter_by(creator_id=user.id).order_by(PendingVideo.created_at.desc()).all()
    else:
        # Editors see only their uploads
        videos = PendingVideo.query.filter_by(uploader_id=user.id).order_by(PendingVideo.created_at.desc()).all()
    
    # Group videos by status for better organization
    pending_videos = [v for v in videos if v.status == 'pending']
    approved_videos = [v for v in videos if v.status == 'approved']
    rejected_videos = [v for v in videos if v.status == 'rejected']
    
    return render_template('my_videos.html', 
                         user=user, 
                         videos=videos,
                         pending_videos=pending_videos,
                         approved_videos=approved_videos,
                         rejected_videos=rejected_videos)

@views.route('/upload')
def upload_form():
    """Display video upload form for editors"""
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # Only editors can upload videos
    if user.role != 'editor':
        flash("Access denied. Editor access required.", "danger")
        return redirect(url_for('views.creator_dashboard' if user.role == 'creator' else 'auth.login'))

    # Get list of creators this editor can upload to
    from app.models.invitation import Invitation
    accepted_invitations = Invitation.query.filter_by(
        editor_id=user.id,
        status='accepted'
    ).all()
    
    available_creators = [inv.creator for inv in accepted_invitations]
    
    if not available_creators:
        flash("You need to be invited by a creator before you can upload videos.", "warning")
        return redirect(url_for('views.editor_dashboard'))
    
    return render_template('upload_video.html', user=user, creators=available_creators)