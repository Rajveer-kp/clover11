#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import db, User
from app.routes.youtube_auth import CLIENT_CONFIG, SCOPES

def test_oauth_setup():
    """Test OAuth setup and configuration"""
    print("🔐 Testing OAuth Setup")
    print("=" * 40)
    
    # Test client configuration
    print("📋 Client Configuration:")
    print(f"   Client ID: {CLIENT_CONFIG['web']['client_id'][:20]}...")
    print(f"   Project ID: {CLIENT_CONFIG['web']['project_id']}")
    print(f"   Redirect URIs: {CLIENT_CONFIG['web']['redirect_uris']}")
    print(f"   Scopes: {SCOPES}")
    
    # Test Flask app
    app = create_app()
    
    with app.app_context():
        # Get a test user
        users = User.query.all()
        creator = None
        for user in users:
            if user.role == 'creator':
                creator = user
                break
        
        if not creator:
            print("❌ No creator found")
            return
        
        print(f"✅ Found creator: {creator.name}")
        
        # Test OAuth authorization URL generation
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = creator.id
                sess['user_name'] = creator.name
                sess['user_role'] = creator.role
            
            # Test authorize endpoint
            response = client.get('/youtube/authorize')
            print(f"✅ OAuth authorize endpoint: {response.status_code}")
            
            if response.status_code == 302:
                redirect_url = response.headers.get('Location', '')
                if 'accounts.google.com' in redirect_url:
                    print("✅ Redirects to Google OAuth")
                    print(f"   Redirect URL: {redirect_url[:100]}...")
                else:
                    print(f"❌ Unexpected redirect: {redirect_url}")
            elif response.status_code == 200:
                print("❌ Should redirect to Google OAuth, but returned 200")
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
        
        print("\n🧪 Testing Manual OAuth Flow")
        print("=" * 40)
        
        # Test manual OAuth flow
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = creator.id
                sess['user_name'] = creator.name
                sess['user_role'] = creator.role
            
            # Test callback with fake auth code (will fail but shows the flow)
            fake_callback_url = "/youtube/oauth2callback?code=fake_code&state=fake_state"
            response = client.get(fake_callback_url)
            print(f"✅ OAuth callback test: {response.status_code}")
            
            if response.status_code == 302:
                print("✅ Callback handles redirect properly")
            elif response.status_code == 500:
                print("⚠️  Callback fails with fake credentials (expected)")
            else:
                print(f"❓ Unexpected callback response: {response.status_code}")

if __name__ == "__main__":
    test_oauth_setup()
