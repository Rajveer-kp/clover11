#!/usr/bin/env python3
"""
Test Team Members Count Logic
Verifies that team member count only includes editors with accepted invitations AND YouTube connections.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation

def test_team_members_count():
    """Test the team members count logic for each creator."""
    app = create_app()
    
    with app.app_context():
        print("=== TEAM MEMBERS COUNT TEST ===\n")
        
        # Get all creators
        creators = User.query.filter_by(role='creator').all()
        
        for creator in creators:
            print(f"Creator: {creator.name} ({creator.email})")
            print(f"YouTube Connected: {creator.youtube_connected}")
            if creator.youtube_connected:
                print(f"Channel: {creator.youtube_channel_name}")
            
            # Get accepted invitations
            accepted_invitations = Invitation.query.filter_by(
                creator_id=creator.id,
                status='accepted'
            ).all()
            
            print(f"\nAccepted Invitations: {len(accepted_invitations)}")
            
            # Count editors with YouTube connections
            connected_editors = 0
            for invitation in accepted_invitations:
                editor = invitation.editor
                print(f"  Editor: {editor.name} ({editor.email})")
                print(f"    YouTube Connected: {editor.youtube_connected}")
                if editor.youtube_connected:
                    print(f"    Channel: {editor.youtube_channel_name}")
                    connected_editors += 1
                else:
                    print(f"    No YouTube connection")
                print()
            
            print(f"Team Members (Connected Editors): {connected_editors}")
            print(f"{'='*50}\n")

if __name__ == "__main__":
    test_team_members_count()
