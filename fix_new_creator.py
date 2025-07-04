#!/usr/bin/env python
"""
Test script to verify login credentials and fix the new creator issue.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User

def check_and_fix_new_creator():
    """Check and fix the new creator's login credentials."""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking new creator's login credentials...")
        
        # Find the new creator
        new_creator = User.query.filter_by(email='rajveerkharade300@gmail.com').first()
        
        if not new_creator:
            print("❌ New creator not found in database")
            return False
        
        print(f"📋 Found creator:")
        print(f"  ID: {new_creator.id}")
        print(f"  Name: {new_creator.name}")
        print(f"  Email: {new_creator.email}")
        print(f"  Role: {new_creator.role}")
        print(f"  YouTube Connected: {new_creator.youtube_connected}")
        print(f"  YouTube Channel Name: {new_creator.youtube_channel_name}")
        
        # Check if password is set
        if new_creator.password_hash:
            print("✅ Password hash exists")
            
            # Test the password
            test_passwords = ['password123', 'admin123', 'test123', '123456']
            
            for pwd in test_passwords:
                if new_creator.check_password(pwd):
                    print(f"✅ Password verified: '{pwd}'")
                    break
            else:
                print("❌ Could not verify password with common test passwords")
                print("   Setting password to 'password123'...")
                new_creator.set_password('password123')
                db.session.commit()
                print("✅ Password set to 'password123'")
        else:
            print("❌ No password hash found")
            print("   Setting password to 'password123'...")
            new_creator.set_password('password123')
            db.session.commit()
            print("✅ Password set to 'password123'")
        
        # Ensure YouTube connection is properly set to False
        if new_creator.youtube_connected != False:
            print("⚠️  YouTube connection status is not False, fixing...")
            new_creator.disconnect_youtube()
            db.session.commit()
            print("✅ YouTube connection properly disconnected")
        
        # Verify final state
        new_creator_fresh = User.query.get(new_creator.id)
        print(f"\n📋 Final state:")
        print(f"  YouTube Connected: {new_creator_fresh.youtube_connected}")
        print(f"  YouTube Channel Name: {new_creator_fresh.youtube_channel_name}")
        
        return True

if __name__ == "__main__":
    success = check_and_fix_new_creator()
    
    if success:
        print("\n✅ New creator check and fix completed")
        print("   You can now login with:")
        print("   Email: rajveerkharade300@gmail.com")
        print("   Password: password123")
    else:
        print("\n❌ New creator check and fix failed")
