#!/usr/bin/env python
"""
Debug script to check YouTube connection status for all users.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

def debug_youtube_connections():
    """Debug YouTube connection status for all users."""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Debugging YouTube connections...")
        
        users = User.query.all()
        
        print(f"\nFound {len(users)} users:")
        print("=" * 80)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"YouTube Connected: {user.youtube_connected}")
            print(f"YouTube Channel Name: {user.youtube_channel_name}")
            
            # Check if credentials exist
            creds = user.get_youtube_credentials()
            if creds:
                print(f"Credentials: Token={creds.get('token', 'N/A')[:20]}...")
            else:
                print("Credentials: None")
            
            print("-" * 80)

if __name__ == "__main__":
    debug_youtube_connections()
