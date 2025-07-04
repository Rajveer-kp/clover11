#!/usr/bin/env python
"""
Test script to verify what the new creator (rajveerkharade300@gmail.com) is seeing.
"""

import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

# Test configuration
BASE_URL = 'http://127.0.0.1:5000'

def test_new_creator():
    """Test what the new creator is seeing."""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing new creator's YouTube connection display...")
        
        # Check database state
        new_creator = User.query.filter_by(email='rajveerkharade300@gmail.com').first()
        
        if not new_creator:
            print("❌ New creator not found in database")
            return False
        
        print(f"📋 Database state for new creator:")
        print(f"  ID: {new_creator.id}")
        print(f"  Name: {new_creator.name}")
        print(f"  Email: {new_creator.email}")
        print(f"  YouTube Connected: {new_creator.youtube_connected}")
        print(f"  YouTube Channel Name: {new_creator.youtube_channel_name}")
        
        # Test web interface
        print(f"\n🌐 Testing web interface...")
        
        session = requests.Session()
        
        # Login as new creator
        login_data = {
            'email': 'rajveerkharade300@gmail.com',
            'password': 'password123'  # Assuming default test password
        }
        
        try:
            response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
            
            print(f"   Login response status: {response.status_code}")
            print(f"   Login response headers: {dict(response.headers)}")
            
            if response.status_code == 302:  # Redirect after successful login
                print("✅ Login successful (redirect)")
                
                # Get dashboard
                dashboard_response = session.get(f'{BASE_URL}/creator')
                
                print(f"   Dashboard response status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    content = dashboard_response.text
                    
                    print("✅ Successfully accessed creator dashboard")
                    
                    # Check if it's actually the dashboard or still login page
                    if 'YouTube Channel Connection' in content:
                        print("✅ Actually on dashboard page")
                        
                        # Check YouTube connection display
                        if 'Connected to:' in content:
                            import re
                            match = re.search(r'Connected to: <strong>([^<]+)</strong>', content)
                            if match:
                                displayed_channel = match.group(1).strip()
                                print(f"🎯 Displayed channel name: '{displayed_channel}'")
                                
                                if displayed_channel == 'rajveer Kharade':
                                    print("❌ ISSUE CONFIRMED: New creator is seeing 'rajveer Kharade' channel name")
                                    print("   This suggests there's cached data or incorrect logic")
                                    return False
                                else:
                                    print(f"✅ Correct channel name displayed: '{displayed_channel}'")
                            else:
                                print("⚠️  Could not extract channel name from HTML")
                        elif 'Not connected to YouTube' in content:
                            print("✅ Correctly shows 'Not connected to YouTube'")
                            return True
                        else:
                            print("⚠️  YouTube connection status unclear")
                            
                            # Save HTML for debugging
                            with open('debug_dashboard.html', 'w', encoding='utf-8') as f:
                                f.write(content)
                            print("   Dashboard HTML saved to debug_dashboard.html")
                    else:
                        print("❌ Still on login page, not dashboard")
                        with open('debug_login_page.html', 'w', encoding='utf-8') as f:
                            f.write(content)
                        print("   Login page HTML saved to debug_login_page.html")
                        return False
                
                else:
                    print(f"❌ Dashboard not accessible (status: {dashboard_response.status_code})")
                    return False
            else:
                print(f"❌ Login failed (status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"💥 Error during web test: {e}")
            return False
        
        return True

if __name__ == "__main__":
    success = test_new_creator()
    
    if success:
        print("\n✅ New creator test completed successfully")
    else:
        print("\n❌ New creator test failed - issue confirmed")
