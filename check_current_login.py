#!/usr/bin/env python
"""
Test script to help debug what user you're currently logged in as.
"""

import requests

BASE_URL = 'http://127.0.0.1:5000'

def check_current_login():
    """Check which user is currently logged in through the browser."""
    
    print("🔍 Checking current login status...")
    print("\n📋 INSTRUCTIONS:")
    print("1. Open your browser and go to: http://127.0.0.1:5000/creator")
    print("2. If you see a login page, login with the account you want to test")
    print("3. If you see the dashboard, note what it shows for YouTube connection")
    print("4. Then run this test to check the API response")
    
    # Test with a fresh session (simulating browser)
    session = requests.Session()
    
    print("\n🌐 Testing YouTube status API without login (should fail)...")
    api_response = session.get(f'{BASE_URL}/youtube/api/youtube/status')
    
    if api_response.status_code == 200:
        try:
            data = api_response.json()
            print(f"✅ API Response: {data}")
            print("⚠️  WARNING: API returned data without login - this shouldn't happen!")
        except:
            print(f"❌ Invalid response: {api_response.text[:100]}...")
    else:
        print(f"✅ API correctly requires login (status: {api_response.status_code})")
    
    print(f"\n📋 To test your specific login:")
    print(f"   1. Open browser to: {BASE_URL}/login")
    print(f"   2. Login with the account you're having issues with")
    print(f"   3. Go to: {BASE_URL}/youtube/api/youtube/status")
    print(f"   4. Check what JSON response you get")
    print(f"   5. It should match the user you logged in as, not 'rajveer Kharade'")
    
    print(f"\n🛠️  To clear browser cache and test properly:")
    print(f"   1. Open browser developer tools (F12)")
    print(f"   2. Right-click refresh button and select 'Empty Cache and Hard Reload'")
    print(f"   3. Or use Incognito/Private mode")
    print(f"   4. Login again and test")
    
    # Test all possible creator logins
    print(f"\n🧪 Testing all creator accounts:")
    
    test_creators = [
        {'email': 'rajveerkharade@gmail.com', 'name': 'Original Creator'},
        {'email': 'rajveerkharade30@gmail.com', 'name': 'Creator 30'},
        {'email': 'rajveerkharade300@gmail.com', 'name': 'Creator 300'},
        {'email': 'creator@test.com', 'name': 'Test Creator'},
    ]
    
    for creator in test_creators:
        print(f"\n📋 Testing {creator['name']} ({creator['email']}):")
        
        test_session = requests.Session()
        
        login_data = {
            'email': creator['email'],
            'password': 'password123'
        }
        
        response = test_session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
        
        if response.status_code == 302:
            api_response = test_session.get(f'{BASE_URL}/youtube/api/youtube/status')
            
            if api_response.status_code == 200:
                try:
                    data = api_response.json()
                    print(f"   ✅ Login successful")
                    print(f"   📊 YouTube Connected: {data.get('connected')}")
                    print(f"   📊 Channel Name: '{data.get('channel_name')}'")
                    
                    if data.get('channel_name') == 'rajveer Kharade':
                        if creator['email'] == 'rajveerkharade@gmail.com':
                            print(f"   ✅ Correct - this is the original creator")
                        else:
                            print(f"   ❌ WRONG! This user shouldn't see 'rajveer Kharade'")
                    
                except Exception as e:
                    print(f"   ❌ JSON error: {e}")
            else:
                print(f"   ❌ API failed: {api_response.status_code}")
        else:
            print(f"   ❌ Login failed: {response.status_code}")

if __name__ == "__main__":
    check_current_login()
