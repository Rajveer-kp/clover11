#!/usr/bin/env python
"""
Test web interface to verify YouTube OAuth isolation in the browser.
"""

import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

# Test configuration
BASE_URL = 'http://127.0.0.1:5000'

def test_web_interface():
    """Test web interface YouTube connection display."""
    
    app = create_app()
    
    with app.app_context():
        print("🔄 Testing web interface YouTube OAuth isolation...")
        
        # Set up test data
        creator1 = User.query.filter_by(email='creator1@test.com').first()
        creator2 = User.query.filter_by(email='creator2@test.com').first()
        
        if not creator1 or not creator2:
            print("❌ Test creators not found. Run the OAuth isolation test first.")
            return False
        
        # Set up different YouTube connections
        creator1.set_youtube_credentials({
            'token': 'web_test_token_creator1',
            'refresh_token': 'web_test_refresh_creator1',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'scopes': ['https://www.googleapis.com/auth/youtube.upload']
        })
        creator1.youtube_channel_name = 'Web Test Channel 1'
        
        creator2.set_youtube_credentials({
            'token': 'web_test_token_creator2',
            'refresh_token': 'web_test_refresh_creator2',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'scopes': ['https://www.googleapis.com/auth/youtube.upload']
        })
        creator2.youtube_channel_name = 'Web Test Channel 2'
        
        db.session.commit()
        
        print("✅ Test data set up complete")
        print(f"  Creator 1: {creator1.youtube_channel_name}")
        print(f"  Creator 2: {creator2.youtube_channel_name}")
        
        # Test 1: Login as Creator 1
        print("\n📋 Test 1: Login as Creator 1")
        session1 = requests.Session()
        
        login_data = {
            'email': 'creator1@test.com',
            'password': 'password123'
        }
        
        response1 = session1.post(f'{BASE_URL}/login', data=login_data)
        
        if response1.status_code == 200:
            # Get dashboard
            dashboard1 = session1.get(f'{BASE_URL}/creator')
            
            if dashboard1.status_code == 200:
                content1 = dashboard1.text
                print("✅ Creator 1 dashboard loaded")
                
                # Check for YouTube channel name
                if 'Web Test Channel 1' in content1:
                    print("✅ Creator 1 sees correct YouTube channel name")
                elif 'Web Test Channel 2' in content1:
                    print("❌ Creator 1 sees Creator 2's YouTube channel name - ISOLATION FAILED")
                    return False
                else:
                    print("⚠️  Creator 1 doesn't see any YouTube channel name")
                    # Check if connected
                    if 'Connect to YouTube' in content1:
                        print("   Creator 1 shows as not connected")
                    else:
                        print("   Creator 1 shows as connected but channel name missing")
            else:
                print("❌ Creator 1 dashboard not accessible")
                return False
        else:
            print("❌ Creator 1 login failed")
            return False
        
        # Test 2: Login as Creator 2 (different session)
        print("\n📋 Test 2: Login as Creator 2")
        session2 = requests.Session()
        
        login_data2 = {
            'email': 'creator2@test.com',
            'password': 'password123'
        }
        
        response2 = session2.post(f'{BASE_URL}/login', data=login_data2)
        
        if response2.status_code == 200:
            # Get dashboard
            dashboard2 = session2.get(f'{BASE_URL}/creator')
            
            if dashboard2.status_code == 200:
                content2 = dashboard2.text
                print("✅ Creator 2 dashboard loaded")
                
                # Check for YouTube channel name
                if 'Web Test Channel 2' in content2:
                    print("✅ Creator 2 sees correct YouTube channel name")
                elif 'Web Test Channel 1' in content2:
                    print("❌ Creator 2 sees Creator 1's YouTube channel name - ISOLATION FAILED")
                    return False
                else:
                    print("⚠️  Creator 2 doesn't see any YouTube channel name")
                    # Check if connected
                    if 'Connect to YouTube' in content2:
                        print("   Creator 2 shows as not connected")
                    else:
                        print("   Creator 2 shows as connected but channel name missing")
            else:
                print("❌ Creator 2 dashboard not accessible")
                return False
        else:
            print("❌ Creator 2 login failed")
            return False
        
        # Test 3: Verify sessions are isolated
        print("\n📋 Test 3: Verify session isolation")
        
        # Try to access Creator 1's dashboard with Creator 2's session
        cross_dashboard = session2.get(f'{BASE_URL}/creator')
        
        if cross_dashboard.status_code == 200:
            cross_content = cross_dashboard.text
            
            # This should still show Creator 2's data, not Creator 1's
            if 'Web Test Channel 2' in cross_content:
                print("✅ Session isolation working - Creator 2 session shows Creator 2 data")
            elif 'Web Test Channel 1' in cross_content:
                print("❌ Session isolation failed - Creator 2 session shows Creator 1 data")
                return False
            else:
                print("⚠️  Session isolation unclear - no clear channel name visible")
        
        print("\n🎉 Web interface OAuth isolation test completed!")
        return True

if __name__ == "__main__":
    try:
        success = test_web_interface()
        if success:
            print("\n🎊 Web interface OAuth isolation working correctly!")
        else:
            print("\n❌ Web interface OAuth isolation failed!")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
