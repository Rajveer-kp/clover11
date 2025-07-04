#!/usr/bin/env python
"""
Clean up test data to ensure fresh testing environment.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation
from app.models.pending_video import PendingVideo

def cleanup_test_data():
    """Clean up test data for fresh testing."""
    
    app = create_app()
    
    with app.app_context():
        print("🧹 Cleaning up test data...")
        
        # Disconnect all test creators from YouTube
        test_creators = User.query.filter(User.email.like('%@test.com')).all()
        
        for creator in test_creators:
            if creator.youtube_connected:
                print(f"  Disconnecting {creator.email} from YouTube")
                creator.disconnect_youtube()
        
        # Delete test videos
        test_videos = PendingVideo.query.filter(
            PendingVideo.title.like('Test Video%')
        ).all()
        
        for video in test_videos:
            print(f"  Deleting test video: {video.title}")
            db.session.delete(video)
        
        # Delete test invitations
        test_invitations = Invitation.query.join(User, Invitation.editor_id == User.id).filter(
            User.email.like('%@test.com')
        ).all()
        
        for invitation in test_invitations:
            print(f"  Deleting test invitation: {invitation.id}")
            db.session.delete(invitation)
        
        # Commit changes
        db.session.commit()
        
        print("✅ Test data cleanup completed!")
        
        # Verify cleanup
        print("\n📋 Verification:")
        for creator in test_creators:
            creator_fresh = User.query.get(creator.id)
            print(f"  {creator.email}: YouTube connected = {creator_fresh.youtube_connected}")
        
        print(f"  Test videos remaining: {PendingVideo.query.filter(PendingVideo.title.like('Test Video%')).count()}")
        print(f"  Test invitations remaining: {len(test_invitations)}")

if __name__ == "__main__":
    cleanup_test_data()
