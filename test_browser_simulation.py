#!/usr/bin/env python3
"""
Browser simulation test to check dashboard behavior
"""

import requests
import json
from bs4 import BeautifulSoup

def test_browser_simulation():
    base_url = "http://localhost:5000"
    
    # Test users who should have different YouTube connection statuses
    test_users = [
        ("rajveerkharade@gmail.com", "test123", "Original Creator - Should be connected"),
        ("rajveerkharade300@gmail.com", "test123", "Creator 300 - Should be disconnected"),
        ("creator@test.com", "test123", "Test Creator - Should be disconnected")
    ]
    
    print("=== BROWSER SIMULATION TEST ===")
    
    for username, password, description in test_users:
        print(f"\n--- {description} ---")
        print(f"Testing user: {username}")
        
        # Create a fresh session for each user
        session = requests.Session()
        
        # Login
        login_data = {
            'email': username,
            'password': password
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed for {username}")
            continue
        
        print(f"✅ Login successful for {username}")
        print(f"🔗 Final URL after login: {login_response.url}")
        
        # Check if we're on the right page
        if "creator" not in login_response.url:
            print(f"❌ Not redirected to creator dashboard. Trying to access it manually.")
            dashboard_response = session.get(f"{base_url}/creator")
        else:
            dashboard_response = login_response
        
        if dashboard_response.status_code != 200:
            print(f"❌ Dashboard access failed")
            continue
        
        # Parse the HTML to see what template variables were passed
        soup = BeautifulSoup(dashboard_response.text, 'html.parser')
        
        # Check YouTube connection status in the template
        youtube_status_element = soup.find('div', class_='youtube-status')
        if youtube_status_element:
            if 'connected-status' in youtube_status_element.get('class', []):
                print(f"📋 Template shows: CONNECTED")
                channel_name = youtube_status_element.find('strong')
                if channel_name:
                    print(f"📋 Channel name in template: {channel_name.text}")
            elif 'disconnected-status' in youtube_status_element.get('class', []):
                print(f"📋 Template shows: NOT CONNECTED")
            else:
                print(f"📋 Template status unclear: {youtube_status_element}")
        else:
            print(f"❌ No YouTube status element found in template")
        
        # Check team members count in template
        stats_number_elements = soup.find_all('div', class_='stats-number')
        for i, element in enumerate(stats_number_elements):
            parent_card = element.find_parent('div', class_='card')
            if parent_card and 'team-card' in parent_card.get('class', []):
                team_count = element.text.strip()
                print(f"📋 Template team members count: {team_count}")
                break
        
        # Test the API endpoint to see what it returns
        try:
            api_response = session.get(f"{base_url}/youtube/api/youtube/status")
            
            if api_response.status_code == 200:
                api_data = api_response.json()
                print(f"🔗 API returns: Connected={api_data.get('connected')}, Channel='{api_data.get('channel_name')}'")
            else:
                print(f"❌ API failed with status {api_response.status_code}")
                print(f"📋 API response text: {api_response.text[:200]}...")
        except Exception as e:
            print(f"❌ API error: {e}")
            print(f"📋 API response text: {api_response.text[:200] if 'api_response' in locals() else 'No response'}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_browser_simulation()
