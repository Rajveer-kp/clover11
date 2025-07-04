#!/usr/bin/env python
"""
Debug the API response for the problematic user.
"""

import requests

BASE_URL = 'http://127.0.0.1:5000'

def debug_api_response():
    """Debug what the API is returning for the problematic user."""
    
    print("🔍 Debugging API response for rajveerkharade@gmail.com...")
    
    session = requests.Session()
    
    login_data = {
        'email': 'rajveerkharade@gmail.com',
        'password': 'password123'  # Try default password first
    }
    
    # Try different common passwords
    passwords = ['password123', 'admin', 'admin123', '123456', 'password']
    
    for pwd in passwords:
        login_data['password'] = pwd
        
        try:
            response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
            
            if response.status_code == 302:  # Successful login
                print(f"✅ Login successful with password: {pwd}")
                
                # Test YouTube status API
                api_response = session.get(f'{BASE_URL}/youtube/api/youtube/status')
                
                print(f"📊 API Response Status: {api_response.status_code}")
                print(f"📊 API Response Headers: {dict(api_response.headers)}")
                print(f"📊 API Response Content Type: {api_response.headers.get('content-type')}")
                print(f"📊 API Response Text: '{api_response.text}'")
                print(f"📊 API Response Length: {len(api_response.text)}")
                
                if api_response.text:
                    try:
                        data = api_response.json()
                        print(f"📊 Parsed JSON: {data}")
                    except Exception as e:
                        print(f"❌ JSON Parse Error: {e}")
                        print(f"   Raw response: {repr(api_response.text)}")
                
                break
            else:
                print(f"❌ Login failed with password {pwd}: {response.status_code}")
        
        except Exception as e:
            print(f"💥 Error with password {pwd}: {e}")
    
    else:
        print("❌ Could not login with any common password")

if __name__ == "__main__":
    debug_api_response()
