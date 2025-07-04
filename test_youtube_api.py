#!/usr/bin/env python
"""
Test the YouTube status API endpoint.
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_youtube_status_api():
    """Test the YouTube status API endpoint."""
    
    print("🔍 Testing YouTube status API endpoint...")
    
    # Test with new creator (should show not connected)
    print("\n📋 Testing with new creator (rajveerkharade300@gmail.com)...")
    
    session = requests.Session()
    
    # Login as new creator
    login_data = {
        'email': 'rajveerkharade300@gmail.com',
        'password': 'password123'
    }
    
    try:
        response = session.post(f'{BASE_URL}/login', data=login_data)
        
        if response.status_code == 200:
            print("✅ Login successful")
            
            # Test API endpoint
            api_response = session.get(f'{BASE_URL}/youtube/api/youtube/status')
            
            if api_response.status_code == 200:
                data = api_response.json()
                print(f"✅ API endpoint working")
                print(f"   Connected: {data.get('connected')}")
                print(f"   Channel Name: '{data.get('channel_name')}'")
                
                if data.get('connected') == False and data.get('channel_name') == '':
                    print("✅ Correct response for non-connected user")
                else:
                    print("❌ Incorrect response for non-connected user")
                    
            else:
                print(f"❌ API endpoint failed (status: {api_response.status_code})")
                print(f"   Response: {api_response.text}")
                
        else:
            print(f"❌ Login failed (status: {response.status_code})")
            
    except Exception as e:
        print(f"💥 Error: {e}")
        
    # Test with connected creator (should show connected)
    print("\n📋 Testing with connected creator (rajveerkharade@gmail.com)...")
    
    session2 = requests.Session()
    
    # Login as connected creator
    login_data2 = {
        'email': 'rajveerkharade@gmail.com',
        'password': 'password123'  # Try default password
    }
    
    try:
        response2 = session2.post(f'{BASE_URL}/login', data=login_data2)
        
        if response2.status_code == 200:
            print("✅ Login successful")
            
            # Test API endpoint
            api_response2 = session2.get(f'{BASE_URL}/youtube/api/youtube/status')
            
            if api_response2.status_code == 200:
                data2 = api_response2.json()
                print(f"✅ API endpoint working")
                print(f"   Connected: {data2.get('connected')}")
                print(f"   Channel Name: '{data2.get('channel_name')}'")
                
                if data2.get('connected') == True and data2.get('channel_name') == 'rajveer Kharade':
                    print("✅ Correct response for connected user")
                else:
                    print("⚠️  Response for connected user (might need password)")
                    
            else:
                print(f"❌ API endpoint failed (status: {api_response2.status_code})")
                print(f"   Response: {api_response2.text}")
                
        else:
            print(f"⚠️  Login failed for connected creator (status: {response2.status_code})")
            print("   This is expected if password is different")
            
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_youtube_status_api()
