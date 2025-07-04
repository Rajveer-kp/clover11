#!/usr/bin/env python
"""
Test script to check what the YouTube status API is returning for different users.
"""

import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

BASE_URL = 'http://127.0.0.1:5000'

def test_api_for_all_creators():
    """Test the YouTube status API for all creator accounts."""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing YouTube status API for all creators...")
        
        # Get all creator accounts
        creators = User.query.filter_by(role='creator').all()
        
        print(f"\nFound {len(creators)} creators:")
        
        for creator in creators:
            print(f"\n📋 Testing Creator: {creator.email}")
            print(f"   Name: {creator.name}")
            print(f"   YouTube Connected (DB): {creator.youtube_connected}")
            print(f"   YouTube Channel (DB): {creator.youtube_channel_name}")
            
            # Try to login and test API
            session = requests.Session()
            
            login_data = {
                'email': creator.email,
                'password': 'password123'  # Default test password
            }
            
            try:
                # Login
                response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
                
                if response.status_code == 302:  # Successful login redirect
                    print("   ✅ Login successful")
                    
                    # Test YouTube status API
                    api_response = session.get(f'{BASE_URL}/youtube/api/youtube/status')
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        print(f"   📊 API Response:")
                        print(f"      Connected: {data.get('connected')}")
                        print(f"      Channel Name: '{data.get('channel_name')}'")
                        
                        # Check if API matches database
                        if data.get('connected') == creator.youtube_connected:
                            print("   ✅ API matches database connection status")
                        else:
                            print("   ❌ API doesn't match database connection status")
                        
                        if data.get('channel_name') == (creator.youtube_channel_name or ''):
                            print("   ✅ API matches database channel name")
                        else:
                            print("   ❌ API doesn't match database channel name")
                            print(f"      Expected: '{creator.youtube_channel_name or ''}'")
                            print(f"      Got: '{data.get('channel_name')}'")
                            
                    else:
                        print(f"   ❌ API request failed: {api_response.status_code}")
                        print(f"   Response: {api_response.text}")
                        
                else:
                    print(f"   ❌ Login failed: {response.status_code}")
                    # Try to see if it's a password issue
                    if response.status_code == 200:
                        print("   (Likely wrong password - user might need password reset)")
                    
            except Exception as e:
                print(f"   💥 Error: {e}")

if __name__ == "__main__":
    test_api_for_all_creators()
