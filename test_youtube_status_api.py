#!/usr/bin/env python3
"""
Test script to verify the YouTube status API endpoint for different users
"""

import requests
import json

def test_youtube_api():
    base_url = "http://localhost:5000"
    
    # Test users (username, password)
    test_users = [
        ("rajveer", "test123"),
        ("Test Creator 1", "test123"),
        ("Test Creator 2", "test123")
    ]
    
    print("=== TESTING YOUTUBE STATUS API ===")
    
    for username, password in test_users:
        print(f"\n--- Testing user: {username} ---")
        
        # Create a session
        session = requests.Session()
        
        # Login
        login_data = {
            'username': username,
            'password': password
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data)
        
        if "dashboard" not in login_response.url:
            print(f"Login failed for {username}")
            continue
        
        print(f"Login successful for {username}")
        
        # Test YouTube status API
        try:
            status_response = session.get(f"{base_url}/youtube/api/youtube/status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"YouTube Status API Response: {status_data}")
            else:
                print(f"YouTube Status API failed with status {status_response.status_code}")
        except Exception as e:
            print(f"Error calling YouTube Status API: {e}")
        
        # Check the dashboard page to see what template variables are passed
        try:
            dashboard_response = session.get(f"{base_url}/creator")
            if dashboard_response.status_code == 200:
                # Look for specific patterns in the response
                if "Connected to:" in dashboard_response.text:
                    print("Dashboard shows: Connected")
                elif "Not connected to YouTube" in dashboard_response.text:
                    print("Dashboard shows: Not connected")
                else:
                    print("Dashboard connection status unclear")
            else:
                print(f"Dashboard access failed with status {dashboard_response.status_code}")
        except Exception as e:
            print(f"Error accessing dashboard: {e}")

if __name__ == "__main__":
    test_youtube_api()
