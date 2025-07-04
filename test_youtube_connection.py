#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import db, User
import requests
import json

def test_youtube_connection():
    """Test YouTube connection status"""
    print("🔍 Testing YouTube Connection Status")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        # Get a test user
        users = User.query.all()
        if not users:
            print("❌ No users found in database")
            return
        
        creator = None
        for user in users:
            if user.role == 'creator':
                creator = user
                break
        
        if not creator:
            print("❌ No creator found in database")
            return
        
        print(f"✅ Testing with creator: {creator.name} ({creator.email})")
        
        # Test with Flask test client
        with app.test_client() as client:
            # Set up session
            with client.session_transaction() as sess:
                sess['user_id'] = creator.id
                sess['user_name'] = creator.name
                sess['user_role'] = creator.role
                # Simulate YouTube connection
                sess['credentials'] = {
                    'token': 'test_token',
                    'refresh_token': 'test_refresh',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                    'client_id': 'test_client_id',
                    'client_secret': 'test_client_secret',
                    'scopes': ['https://www.googleapis.com/auth/youtube.upload']
                }
                sess['youtube_channel_name'] = 'Test Channel'
                
                print("✅ Set up test session with YouTube credentials")
            
            # Test debug endpoint
            response = client.get('/youtube/debug-session')
            print(f"✅ Debug endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"   Session data: {data}")
            
            # Test YouTube status API
            response = client.get('/youtube/api/youtube-status')
            print(f"✅ YouTube status API: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"   API response: {data}")
            
            # Test creator dashboard
            response = client.get('/creator')
            print(f"✅ Creator dashboard: {response.status_code}")
            if response.status_code == 200:
                # Check if the dashboard has the YouTube connection info
                html_content = response.get_data(as_text=True)
                if 'Connected to:' in html_content:
                    print("✅ Dashboard shows YouTube connection")
                elif 'Not connected to YouTube' in html_content:
                    print("❌ Dashboard shows NOT connected")
                else:
                    print("❓ Dashboard connection status unclear")
                    
                # Check for specific elements
                if 'youtube_connected=True' in html_content or 'Connected to: <strong>Test Channel</strong>' in html_content:
                    print("✅ Template variables correctly passed")
                else:
                    print("❌ Template variables not correctly passed")
        
        print("\n" + "=" * 40)
        print("🔧 TESTING WITHOUT CREDENTIALS")
        print("=" * 40)
        
        # Test without credentials
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = creator.id
                sess['user_name'] = creator.name
                sess['user_role'] = creator.role
                # No credentials this time
                print("✅ Set up session WITHOUT YouTube credentials")
            
            # Test YouTube status API
            response = client.get('/youtube/api/youtube-status')
            print(f"✅ YouTube status API: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"   API response: {data}")
            
            # Test creator dashboard
            response = client.get('/creator')
            print(f"✅ Creator dashboard: {response.status_code}")
            if response.status_code == 200:
                html_content = response.get_data(as_text=True)
                if 'Not connected to YouTube' in html_content:
                    print("✅ Dashboard correctly shows NOT connected")
                elif 'Connected to:' in html_content:
                    print("❌ Dashboard incorrectly shows connected")
                else:
                    print("❓ Dashboard connection status unclear")

if __name__ == "__main__":
    test_youtube_connection()
