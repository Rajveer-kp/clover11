#!/usr/bin/env python3
"""
Quick user account checker - shows which users have YouTube connections
"""

from app import create_app, db
from app.models.user import User

def show_user_accounts():
    app = create_app()
    
    with app.app_context():
        print("🔍 CURRENT USER ACCOUNTS AND YOUTUBE STATUS")
        print("=" * 60)
        
        users = User.query.all()
        
        print(f"\n📊 Total users in database: {len(users)}")
        print("\n🎯 CREATOR ACCOUNTS (these can have YouTube connections):")
        print("-" * 60)
        
        creators = [u for u in users if u.role == 'creator']
        connected_creators = []
        
        for user in creators:
            status = "✅ CONNECTED" if user.youtube_connected else "❌ Not Connected"
            channel = f" to '{user.youtube_channel_name}'" if user.youtube_channel_name else ""
            
            print(f"📧 Email: {user.email}")
            print(f"👤 Name: {user.name}")
            print(f"🔗 YouTube: {status}{channel}")
            print(f"🆔 User ID: {user.id}")
            
            if user.youtube_connected:
                connected_creators.append(user)
            
            print("-" * 40)
        
        print(f"\n🎉 ACCOUNTS WITH YOUTUBE CONNECTIONS:")
        if connected_creators:
            for user in connected_creators:
                print(f"✅ Login with: {user.email} / test123")
                print(f"   Channel: {user.youtube_channel_name}")
        else:
            print("❌ No creators have YouTube connections currently.")
            print("💡 You need to connect a YouTube account first!")
        
        print(f"\n📝 EDITOR ACCOUNTS (for testing uploads):")
        print("-" * 60)
        editors = [u for u in users if u.role == 'editor']
        for user in editors:
            print(f"📧 {user.email} (Name: {user.name})")
        
        print(f"\n🔧 QUICK TEST INSTRUCTIONS:")
        print("1. Open browser: http://localhost:5000/login")
        print("2. Clear cache (Ctrl+Shift+Delete) or use Incognito mode")
        if connected_creators:
            print(f"3. Login with: {connected_creators[0].email} / test123")
            print("4. Should show: 'Connected to: [channel name]'")
        else:
            print("3. Login with any creator account")
            print("4. Click 'Connect YouTube' to set up YouTube connection")

if __name__ == "__main__":
    show_user_accounts()
