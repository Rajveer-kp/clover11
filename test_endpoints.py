#!/usr/bin/env python3

import requests
import json

# Test the Flask application endpoints
BASE_URL = "http://127.0.0.1:5000"

def test_endpoints():
    """Test the API endpoints"""
    print("Testing Flask Application Endpoints")
    print("=" * 40)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Check if app is running
    try:
        response = session.get(f"{BASE_URL}/")
        print(f"✓ App running: {response.status_code}")
    except Exception as e:
        print(f"✗ App not running: {e}")
        return
    
    # Test 2: Check if register page loads
    try:
        response = session.get(f"{BASE_URL}/register")
        print(f"✓ Register page: {response.status_code}")
    except Exception as e:
        print(f"✗ Register page error: {e}")
    
    # Test 3: Create a test user
    try:
        user_data = {
            'name': 'Test Creator',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'creator'
        }
        response = session.post(f"{BASE_URL}/register", data=user_data)
        print(f"✓ User creation: {response.status_code}")
    except Exception as e:
        print(f"✗ User creation error: {e}")
    
    # Test 4: Login
    try:
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = session.post(f"{BASE_URL}/login", data=login_data)
        print(f"✓ Login: {response.status_code}")
    except Exception as e:
        print(f"✗ Login error: {e}")
    
    # Test 5: Check authenticated endpoints
    print("\nTesting authenticated endpoints:")
    
    # Test YouTube status endpoint
    try:
        response = session.get(f"{BASE_URL}/youtube/api/youtube-status")
        print(f"✓ YouTube status endpoint: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {data}")
            except:
                print(f"  Response (not JSON): {response.text[:100]}...")
    except Exception as e:
        print(f"✗ YouTube status error: {e}")
    
    # Test notifications count endpoint
    try:
        response = session.get(f"{BASE_URL}/youtube/api/notifications/count")
        print(f"✓ Notifications endpoint: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {data}")
            except:
                print(f"  Response (not JSON): {response.text[:100]}...")
    except Exception as e:
        print(f"✗ Notifications error: {e}")
    
    # Test dashboard access
    try:
        response = session.get(f"{BASE_URL}/dashboard")
        print(f"✓ Dashboard access: {response.status_code}")
    except Exception as e:
        print(f"✗ Dashboard error: {e}")

if __name__ == "__main__":
    test_endpoints()
