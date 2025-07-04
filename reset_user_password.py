#!/usr/bin/env python
"""
Reset password for the problematic user account.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

def reset_user_password():
    """Reset password for rajveerkharade@gmail.com."""
    
    app = create_app()
    
    with app.app_context():
        print("🔐 Resetting password for rajveerkharade@gmail.com...")
        
        user = User.query.filter_by(email='rajveerkharade@gmail.com').first()
        
        if not user:
            print("❌ User not found")
            return False
        
        print(f"📋 Found user:")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   YouTube Connected: {user.youtube_connected}")
        print(f"   YouTube Channel: {user.youtube_channel_name}")
        
        # Reset password to default
        print("\n🔑 Resetting password to 'password123'...")
        user.set_password('password123')
        db.session.commit()
        
        print("✅ Password reset successfully!")
        print("   You can now login with:")
        print("   Email: rajveerkharade@gmail.com")
        print("   Password: password123")
        
        return True

if __name__ == "__main__":
    reset_user_password()
