#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import db, User
from app.models.pending_video import PendingVideo
import requests
import json

def test_with_flask_context():
    """Test the endpoints using Flask application context"""
    print("Testing with Flask Application Context")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        # Check existing users
        users = User.query.all()
        print(f"Existing users: {len(users)}")
        for user in users:
            print(f"  - {user.name} ({user.email}) - {user.role}")
        
        # Check pending videos
        pending_videos = PendingVideo.query.all()
        print(f"Pending videos: {len(pending_videos)}")
        
        # Test the endpoints with a test client
        with app.test_client() as client:
            print("\nTesting with test client:")
            
            # Test login page
            response = client.get('/login')
            print(f"✓ Login page: {response.status_code}")
            
            # If we have a user, test login
            if users:
                test_user = users[0]
                print(f"Testing login with user: {test_user.email}")
                
                # Create a session and login
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                    sess['user_name'] = test_user.name
                    sess['user_role'] = test_user.role
                
                # Test authenticated endpoints
                print("\nTesting authenticated endpoints:")
                
                # Test YouTube status
                response = client.get('/youtube/api/youtube-status')
                print(f"✓ YouTube status: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.get_json()
                        print(f"  Response: {data}")
                    except:
                        print(f"  Response (HTML): {response.data[:100]}...")
                
                # Test notifications count
                response = client.get('/youtube/api/notifications/count')
                print(f"✓ Notifications count: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.get_json()
                        print(f"  Response: {data}")
                    except:
                        print(f"  Response (HTML): {response.data[:100]}...")
                
                # Test dashboard
                response = client.get('/dashboard')
                print(f"✓ Dashboard: {response.status_code}")
                
                # Test creator dashboard specifically
                if test_user.role == 'creator':
                    response = client.get('/creator')
                    print(f"✓ Creator dashboard: {response.status_code}")
                elif test_user.role == 'editor':
                    response = client.get('/editor')
                    print(f"✓ Editor dashboard: {response.status_code}")
                
            else:
                print("No users found in database")

if __name__ == "__main__":
    test_with_flask_context()
