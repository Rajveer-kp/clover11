#!/usr/bin/env python3
"""
Migration script to add created_at column to user table
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Add created_at column to user table if it doesn't exist."""
    try:
        # Connect to the database
        conn = sqlite3.connect('instance/site.db')
        cursor = conn.cursor()
        
        # Check if created_at column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("Adding created_at column to user table...")
            
            # Add the created_at column with a default value
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT '{current_time}'")
            
            # Update existing users with current timestamp
            cursor.execute(f"UPDATE user SET created_at = '{current_time}' WHERE created_at IS NULL")
            
            conn.commit()
            print("✅ Successfully added created_at column")
        else:
            print("✅ created_at column already exists")
        
        # Verify the migration
        cursor.execute("SELECT name, email, created_at FROM user LIMIT 3")
        users = cursor.fetchall()
        print(f"✅ Verified migration - found {len(users)} users with created_at timestamps")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🔄 Starting database migration...")
    success = migrate_database()
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
