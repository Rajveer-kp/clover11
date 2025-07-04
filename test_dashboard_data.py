#!/usr/bin/env python3
"""
Test script to verify the dashboard API endpoint and database state
"""

import requests
import json
from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation

def test_dashboard_data():
    app = create_app()
    
    with app.app_context():
        print("=== DASHBOARD DATA TEST ===")
        
        # Check all users and their YouTube connection status
        users = User.query.all()
        print(f"\nAll users in database:")
        for user in users:
            print(f"  {user.name} ({user.role}): YouTube connected = {user.youtube_connected}, Channel = {user.youtube_channel_name}")
        
        # Check invitations
        print(f"\nAll invitations:")
        invitations = Invitation.query.all()
        for inv in invitations:
            print(f"  {inv.creator.name} -> {inv.editor.name}: Status = {inv.status}")
        
        # Test the creator dashboard logic for each creator
        creators = User.query.filter_by(role='creator').all()
        
        for creator in creators:
            print(f"\n=== Testing creator: {creator.name} ===")
            
            # Simulate the team member count logic from views.py
            accepted_invitations = Invitation.query.filter_by(
                creator_id=creator.id,
                status='accepted'
            ).all()
            
            print(f"Accepted invitations for {creator.name}:")
            team_members = 0
            for invitation in accepted_invitations:
                youtube_status = invitation.editor.youtube_connected
                print(f"  - {invitation.editor.name}: YouTube connected = {youtube_status}")
                if youtube_status:
                    team_members += 1
            
            print(f"Team members count (with YouTube): {team_members}")
            print(f"Creator YouTube status: {creator.youtube_connected}")
            print(f"Creator YouTube channel: {creator.youtube_channel_name}")

if __name__ == "__main__":
    test_dashboard_data()
