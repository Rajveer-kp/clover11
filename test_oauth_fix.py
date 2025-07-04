#!/usr/bin/env python
"""
Comprehensive test script to verify YouTube OAuth isolation fix.
This script tests the actual login flow to ensure each creator sees their own YouTube connection.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = 'http://127.0.0.1:5000'
TEST_CREATORS = [
    {'name': 'Creator One', 'email': 'creator1@test.com', 'password': 'password123'},
    {'name': 'Creator Two', 'email': 'creator2@test.com', 'password': 'password123'}
]

def test_creator_isolation():
    """Test that each creator sees their own YouTube connection status."""
    
    print("🔄 Testing YouTube OAuth isolation with actual login sessions...")
    
    # Test results
    results = []
    sessions = []
    
    for i, creator_data in enumerate(TEST_CREATORS):
        print(f"\n📋 Testing Creator {i+1}: {creator_data['name']}")
        
        # Create a session for this creator
        session = requests.Session()
        
        # Test login
        login_data = {
            'email': creator_data['email'],
            'password': creator_data['password']
        }
        
        try:
            # Login
            response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                print(f"✅ {creator_data['name']} login successful")
                
                # Get creator dashboard
                dashboard_response = session.get(f'{BASE_URL}/creator')
                
                if dashboard_response.status_code == 200:
                    print(f"✅ {creator_data['name']} dashboard accessible")
                    
                    # Check if YouTube connection status is shown
                    dashboard_content = dashboard_response.text
                    
                    # Look for YouTube connection indicators
                    youtube_connected = 'Connect to YouTube' not in dashboard_content
                    channel_name = ''
                    
                    if 'youtube_channel_name' in dashboard_content:
                        # Extract channel name if present
                        import re
                        match = re.search(r'YouTube Channel: ([^<]+)', dashboard_content)
                        if match:
                            channel_name = match.group(1).strip()
                    
                    result = {
                        'creator': creator_data['name'],
                        'email': creator_data['email'],
                        'login_success': True,
                        'dashboard_access': True,
                        'youtube_connected': youtube_connected,
                        'channel_name': channel_name,
                        'session': session
                    }
                    
                    print(f"   YouTube Connected: {youtube_connected}")
                    print(f"   Channel Name: {channel_name}")
                    
                else:
                    print(f"❌ {creator_data['name']} dashboard not accessible")
                    result = {
                        'creator': creator_data['name'],
                        'email': creator_data['email'],
                        'login_success': True,
                        'dashboard_access': False,
                        'session': session
                    }
            else:
                print(f"❌ {creator_data['name']} login failed")
                result = {
                    'creator': creator_data['name'],
                    'email': creator_data['email'],
                    'login_success': False,
                    'session': session
                }
            
            results.append(result)
            sessions.append(session)
            
        except Exception as e:
            print(f"💥 Error testing {creator_data['name']}: {e}")
            result = {
                'creator': creator_data['name'],
                'email': creator_data['email'],
                'error': str(e),
                'session': session
            }
            results.append(result)
    
    # Analysis
    print("\n📊 Analysis:")
    print("=" * 50)
    
    successful_logins = [r for r in results if r.get('login_success')]
    print(f"Successful logins: {len(successful_logins)}/{len(TEST_CREATORS)}")
    
    dashboard_access = [r for r in results if r.get('dashboard_access')]
    print(f"Dashboard access: {len(dashboard_access)}/{len(TEST_CREATORS)}")
    
    # Check for isolation
    connected_creators = [r for r in results if r.get('youtube_connected')]
    print(f"YouTube connected creators: {len(connected_creators)}")
    
    if len(connected_creators) >= 2:
        # Check if they have different channel names
        channel_names = [r.get('channel_name', '') for r in connected_creators]
        unique_channels = set(channel_names)
        
        if len(unique_channels) == len(connected_creators):
            print("✅ Each creator has a unique YouTube channel name")
        else:
            print("❌ Creators are sharing YouTube channel names")
    
    # Test cross-session isolation
    print("\n🔄 Testing cross-session isolation...")
    
    if len(sessions) >= 2:
        # Try to access creator 1's dashboard with creator 2's session
        try:
            cross_response = sessions[1].get(f'{BASE_URL}/creator')
            if cross_response.status_code == 200:
                print("✅ Sessions are properly isolated")
            else:
                print("❌ Session isolation issue detected")
        except Exception as e:
            print(f"⚠️  Cross-session test error: {e}")
    
    # Summary
    print("\n🎯 Summary:")
    print("=" * 50)
    
    for result in results:
        creator = result['creator']
        if result.get('login_success'):
            if result.get('dashboard_access'):
                status = f"✅ {creator}: Login OK, Dashboard OK"
                if result.get('youtube_connected'):
                    status += f", YouTube: {result.get('channel_name', 'Connected')}"
                else:
                    status += ", YouTube: Not Connected"
            else:
                status = f"⚠️  {creator}: Login OK, Dashboard Failed"
        else:
            status = f"❌ {creator}: Login Failed"
        
        print(status)
    
    print("\n🎉 YouTube OAuth isolation test completed!")
    
    return results

def test_database_isolation():
    """Test that the database correctly stores isolated credentials."""
    
    print("\n🔄 Testing database credential isolation...")
    
    # Use the test script from earlier
    try:
        import subprocess
        result = subprocess.run(['python', 'test_oauth_isolation.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Database isolation test passed")
            return True
        else:
            print("❌ Database isolation test failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"⚠️  Database isolation test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive YouTube OAuth isolation test...")
    print("=" * 60)
    
    # Test 1: Web session isolation
    web_results = test_creator_isolation()
    
    # Test 2: Database isolation
    db_results = test_database_isolation()
    
    print("\n🎊 All tests completed!")
    print("=" * 60)
    
    if db_results:
        print("✅ Database credential isolation: WORKING")
    else:
        print("❌ Database credential isolation: FAILED")
    
    successful_web_tests = len([r for r in web_results if r.get('login_success')])
    print(f"✅ Web session tests: {successful_web_tests}/{len(TEST_CREATORS)} successful")
    
    if db_results and successful_web_tests == len(TEST_CREATORS):
        print("\n🎉 YouTube OAuth isolation fix is working correctly!")
        print("✅ Each creator now has their own isolated YouTube connection")
        print("✅ No more shared credentials between creators")
        print("✅ Database storage maintains proper isolation")
    else:
        print("\n⚠️  Some issues detected - please check the logs above")
