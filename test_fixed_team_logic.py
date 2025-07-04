#!/usr/bin/env python3
"""
Test script to verify the fixed team member count logic
"""

from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation

def test_fixed_team_logic():
    app = create_app()
    
    with app.app_context():
        print("=== TESTING FIXED TEAM MEMBER LOGIC ===")
        
        # Check all users and their YouTube connection status
        users = User.query.all()
        print(f"\nAll users in database:")
        for user in users:
            print(f"  {user.name} ({user.role}): YouTube connected = {user.youtube_connected}")
        
        # Check invitations
        print(f"\nAll invitations:")
        invitations = Invitation.query.all()
        for inv in invitations:
            print(f"  {inv.creator.name} -> {inv.editor.name}: Status = {inv.status}")
        
        # Test the FIXED creator dashboard logic for each creator
        creators = User.query.filter_by(role='creator').all()
        
        for creator in creators:
            print(f"\n=== Testing creator: {creator.name} (ID: {creator.id}) ===")
            
            # Use the NEW logic from views.py: count ALL accepted invitations
            accepted_invitations = Invitation.query.filter_by(
                creator_id=creator.id,
                status='accepted'
            ).all()
            
            print(f"Accepted invitations for {creator.name}:")
            for invitation in accepted_invitations:
                print(f"  - {invitation.editor.name} (Editor)")
            
            team_members = len(accepted_invitations)  # NEW LOGIC: just count accepted invitations
            print(f"Team members count (FIXED): {team_members}")
            print(f"Creator YouTube status: {creator.youtube_connected}")

if __name__ == "__main__":
    test_fixed_team_logic()
