#!/usr/bin/env python3
"""
Simulate Creator Dashboard Team Members Count
Tests the exact logic used in creator_dashboard view.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.invitation import Invitation

def simulate_dashboard_logic():
    """Simulate the exact team members logic from creator_dashboard view."""
    app = create_app()
    
    with app.app_context():
        print("=== CREATOR DASHBOARD SIMULATION ===\n")
        
        # Get the main creator (rajveerkharade@gmail.com)
        user = User.query.filter_by(email='rajveerkharade@gmail.com').first()
        
        if not user:
            print("Creator not found!")
            return
        
        print(f"Creator: {user.name} ({user.email})")
        print(f"Role: {user.role}")
        print(f"YouTube Connected: {user.youtube_connected}")
        if user.youtube_connected:
            print(f"Channel: {user.youtube_channel_name}")
        
        # Apply the exact logic from creator_dashboard
        accepted_invitations = Invitation.query.filter_by(
            creator_id=user.id,
            status='accepted'
        ).all()
        
        # Count only editors with active YouTube connections
        team_members = 0
        for invitation in accepted_invitations:
            if invitation.editor.youtube_connected:
                team_members += 1
        
        print(f"\nDashboard Stats:")
        print(f"  Total Accepted Invitations: {len(accepted_invitations)}")
        print(f"  Team Members (YouTube Connected): {team_members}")
        
        print(f"\nEditor Details:")
        for invitation in accepted_invitations:
            editor = invitation.editor
            print(f"  - {editor.name} ({editor.email})")
            print(f"    YouTube Connected: {editor.youtube_connected}")
            if editor.youtube_connected:
                print(f"    Channel: {editor.youtube_channel_name}")
            else:
                print(f"    Status: No YouTube connection")
            print()

if __name__ == "__main__":
    simulate_dashboard_logic()
