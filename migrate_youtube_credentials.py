#!/usr/bin/env python
"""
Migration script to add YouTube credentials fields to User model.
This script adds the new fields needed for per-user YouTube OAuth storage.
"""

import sqlite3
import os
from datetime import datetime

def migrate_youtube_credentials():
    """Add YouTube credentials fields to the User table."""
    
    # Database path
    db_path = os.path.join('instance', 'site.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        migrations_needed = []
        
        if 'youtube_credentials' not in columns:
            migrations_needed.append('youtube_credentials')
        
        if 'youtube_channel_name' not in columns:
            migrations_needed.append('youtube_channel_name')
            
        if 'youtube_connected' not in columns:
            migrations_needed.append('youtube_connected')
        
        if not migrations_needed:
            print("YouTube credentials fields already exist in User table.")
            return True
        
        print(f"Adding fields to User table: {migrations_needed}")
        
        # Add the new columns
        if 'youtube_credentials' in migrations_needed:
            cursor.execute("ALTER TABLE user ADD COLUMN youtube_credentials TEXT")
            print("Added youtube_credentials column")
        
        if 'youtube_channel_name' in migrations_needed:
            cursor.execute("ALTER TABLE user ADD COLUMN youtube_channel_name VARCHAR(200)")
            print("Added youtube_channel_name column")
        
        if 'youtube_connected' in migrations_needed:
            cursor.execute("ALTER TABLE user ADD COLUMN youtube_connected BOOLEAN DEFAULT 0")
            print("Added youtube_connected column")
        
        # Commit the changes
        conn.commit()
        
        print("✅ YouTube credentials migration completed successfully!")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        print("\nUpdated User table schema:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔄 Starting YouTube credentials migration...")
    success = migrate_youtube_credentials()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("Users can now have isolated YouTube OAuth connections.")
    else:
        print("\n💥 Migration failed!")
        print("Please check the error messages above and try again.")
