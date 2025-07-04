#!/usr/bin/env python
"""
Test script to verify YouTube OAuth isolation between creators.
This test ensures that each creator has their own isolated YouTube connection.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation
from app.models.pending_video import PendingVideo
from datetime import datetime
import json

def test_youtube_oauth_isolation():
    """Test that YouTube OAuth connections are isolated between creators."""
    
    app = create_app()
    
    with app.app_context():
        print("🔄 Testing YouTube OAuth isolation...")
        
        # Create or get test creators
        creator1 = User.query.filter_by(email='creator1@test.com').first()
        if not creator1:
            creator1 = User(
                name='Test Creator 1',
                email='creator1@test.com',
                role='creator'
            )
            creator1.set_password('password123')
            db.session.add(creator1)
        
        creator2 = User.query.filter_by(email='creator2@test.com').first()
        if not creator2:
            creator2 = User(
                name='Test Creator 2',
                email='creator2@test.com',
                role='creator'
            )
            creator2.set_password('password123')
            db.session.add(creator2)
        
        db.session.commit()
        
        # Test 1: Initially no YouTube connections
        print("\n📋 Test 1: Initial state - no YouTube connections")
        print(f"Creator 1 YouTube connected: {creator1.youtube_connected}")
        print(f"Creator 2 YouTube connected: {creator2.youtube_connected}")
        
        assert creator1.youtube_connected == False, "Creator 1 should not be connected initially"
        assert creator2.youtube_connected == False, "Creator 2 should not be connected initially"
        print("✅ Test 1 passed: No initial connections")
        
        # Test 2: Connect Creator 1 to YouTube
        print("\n📋 Test 2: Connect Creator 1 to YouTube")
        test_credentials_1 = {
            'token': 'test_token_creator1',
            'refresh_token': 'test_refresh_creator1',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'scopes': ['https://www.googleapis.com/auth/youtube.upload']
        }
        
        creator1.set_youtube_credentials(test_credentials_1)
        creator1.youtube_channel_name = 'Test Channel 1'
        db.session.commit()
        
        # Refresh from database
        creator1 = User.query.get(creator1.id)
        creator2 = User.query.get(creator2.id)
        
        print(f"Creator 1 YouTube connected: {creator1.youtube_connected}")
        print(f"Creator 1 channel name: {creator1.youtube_channel_name}")
        print(f"Creator 2 YouTube connected: {creator2.youtube_connected}")
        
        assert creator1.youtube_connected == True, "Creator 1 should be connected"
        assert creator1.youtube_channel_name == 'Test Channel 1', "Creator 1 should have correct channel name"
        assert creator2.youtube_connected == False, "Creator 2 should still not be connected"
        print("✅ Test 2 passed: Creator 1 connected, Creator 2 isolated")
        
        # Test 3: Connect Creator 2 to YouTube (different credentials)
        print("\n📋 Test 3: Connect Creator 2 to YouTube")
        test_credentials_2 = {
            'token': 'test_token_creator2',
            'refresh_token': 'test_refresh_creator2',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'scopes': ['https://www.googleapis.com/auth/youtube.upload']
        }
        
        creator2.set_youtube_credentials(test_credentials_2)
        creator2.youtube_channel_name = 'Test Channel 2'
        db.session.commit()
        
        # Refresh from database
        creator1 = User.query.get(creator1.id)
        creator2 = User.query.get(creator2.id)
        
        print(f"Creator 1 YouTube connected: {creator1.youtube_connected}")
        print(f"Creator 1 channel name: {creator1.youtube_channel_name}")
        print(f"Creator 2 YouTube connected: {creator2.youtube_connected}")
        print(f"Creator 2 channel name: {creator2.youtube_channel_name}")
        
        assert creator1.youtube_connected == True, "Creator 1 should still be connected"
        assert creator1.youtube_channel_name == 'Test Channel 1', "Creator 1 should have correct channel name"
        assert creator2.youtube_connected == True, "Creator 2 should now be connected"
        assert creator2.youtube_channel_name == 'Test Channel 2', "Creator 2 should have correct channel name"
        print("✅ Test 3 passed: Both creators connected with different credentials")
        
        # Test 4: Verify credentials are different
        print("\n📋 Test 4: Verify credentials isolation")
        creds1 = creator1.get_youtube_credentials()
        creds2 = creator2.get_youtube_credentials()
        
        print(f"Creator 1 token: {creds1['token']}")
        print(f"Creator 2 token: {creds2['token']}")
        
        assert creds1['token'] != creds2['token'], "Tokens should be different"
        assert creds1['refresh_token'] != creds2['refresh_token'], "Refresh tokens should be different"
        print("✅ Test 4 passed: Credentials are properly isolated")
        
        # Test 5: Disconnect Creator 1, verify Creator 2 unaffected
        print("\n📋 Test 5: Disconnect Creator 1, verify Creator 2 unaffected")
        creator1.disconnect_youtube()
        db.session.commit()
        
        # Refresh from database
        creator1 = User.query.get(creator1.id)
        creator2 = User.query.get(creator2.id)
        
        print(f"Creator 1 YouTube connected: {creator1.youtube_connected}")
        print(f"Creator 1 channel name: {creator1.youtube_channel_name}")
        print(f"Creator 2 YouTube connected: {creator2.youtube_connected}")
        print(f"Creator 2 channel name: {creator2.youtube_channel_name}")
        
        assert creator1.youtube_connected == False, "Creator 1 should be disconnected"
        assert creator1.youtube_channel_name is None, "Creator 1 channel name should be None"
        assert creator2.youtube_connected == True, "Creator 2 should still be connected"
        assert creator2.youtube_channel_name == 'Test Channel 2', "Creator 2 should have correct channel name"
        print("✅ Test 5 passed: Creator 1 disconnected, Creator 2 unaffected")
        
        print("\n🎉 All YouTube OAuth isolation tests passed!")
        print("✅ Each creator has their own isolated YouTube connection")
        print("✅ Credentials are stored in database, not shared session")
        print("✅ Connection/disconnection is properly isolated")
        
        return True

if __name__ == "__main__":
    try:
        success = test_youtube_oauth_isolation()
        if success:
            print("\n🎊 YouTube OAuth isolation working correctly!")
        else:
            print("\n❌ YouTube OAuth isolation tests failed!")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
