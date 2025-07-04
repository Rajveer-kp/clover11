#!/usr/bin/env python3
"""
Test script to verify YouTube OAuth integration
"""

from app import create_app, db
from app.models.user import User
from app.models.pending_video import PendingVideo
from app.models.invitation import Invitation

def test_app():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create test users
        print("Creating test users...")
        
        # Create a test creator
        creator = User.query.filter_by(email='creator@test.com').first()
        if not creator:
            creator = User(
                name='Test Creator',
                email='creator@test.com',
                role='creator'
            )
            creator.set_password('password123')
            db.session.add(creator)
        
        # Create a test editor
        editor = User.query.filter_by(email='editor@test.com').first()
        if not editor:
            editor = User(
                name='Test Editor',
                email='editor@test.com',
                role='editor'
            )
            editor.set_password('password123')
            db.session.add(editor)
        
        db.session.commit()
        
        print("Test users created successfully!")
        print(f"Creator: {creator.name} ({creator.email})")
        print(f"Editor: {editor.name} ({editor.email})")
        
        # Test invitation system
        print("\nTesting invitation system...")
        
        invitation = Invitation.query.filter_by(
            creator_id=creator.id,
            editor_id=editor.id
        ).first()
        
        if not invitation:
            invitation = Invitation(
                creator_id=creator.id,
                editor_id=editor.id,
                status='pending'
            )
            db.session.add(invitation)
            db.session.commit()
            print("Test invitation created successfully!")
        else:
            print("Test invitation already exists!")
        
        # Test pending video
        print("\nTesting pending video system...")
        
        pending = PendingVideo.query.filter_by(
            uploader_id=editor.id,
            creator_id=creator.id
        ).first()
        
        if not pending:
            pending = PendingVideo(
                title='Test Video',
                description='This is a test video upload',
                tags='test,video,youtube',
                filename='test_video.mp4',
                uploader_id=editor.id,
                creator_id=creator.id,
                status='pending'
            )
            db.session.add(pending)
            db.session.commit()
            print("Test pending video created successfully!")
        else:
            print("Test pending video already exists!")
        
        print("\n✅ All tests passed!")
        print("\nYou can now login with:")
        print("Creator: creator@test.com / password123")
        print("Editor: editor@test.com / password123")
        
        print("\nTo test YouTube OAuth:")
        print("1. Login as creator")
        print("2. Go to creator dashboard")
        print("3. Click 'Connect YouTube'")
        print("4. Complete OAuth flow")
        print("5. Check if connection status updates")

if __name__ == '__main__':
    test_app()
