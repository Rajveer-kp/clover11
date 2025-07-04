#!/usr/bin/env python3
"""
Reset passwords for test users
"""

from app import create_app, db
from app.models.user import User

def reset_test_passwords():
    app = create_app()
    
    with app.app_context():
        print("=== RESETTING TEST USER PASSWORDS ===")
        
        # Test users to reset
        test_emails = [
            "rajveerkharade@gmail.com",
            "rajveerkharade300@gmail.com", 
            "creator@test.com"
        ]
        
        for email in test_emails:
            user = User.query.filter_by(email=email).first()
            if user:
                user.set_password("test123")
                print(f"✅ Reset password for {user.name} ({email})")
            else:
                print(f"❌ User not found: {email}")
        
        db.session.commit()
        print("\n🔄 All passwords reset to 'test123'")

if __name__ == "__main__":
    reset_test_passwords()
