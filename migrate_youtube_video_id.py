#!/usr/bin/env python3
"""
Migration script to add youtube_video_id field to pending_video table
"""

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import db
from app.models.pending_video import PendingVideo

def migrate_database():
    """Add youtube_video_id column to pending_video table"""
    print("🔄 Running Database Migration")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('pending_video')]
            
            if 'youtube_video_id' in columns:
                print("✅ youtube_video_id column already exists")
                return True
            
            # Add the new column
            print("📝 Adding youtube_video_id column to pending_video table...")
            with db.engine.connect() as connection:
                connection.execute(db.text('ALTER TABLE pending_video ADD COLUMN youtube_video_id VARCHAR(50)'))
                connection.commit()
            
            print("✅ Migration completed successfully!")
            
            # Verify the change
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('pending_video')]
            
            if 'youtube_video_id' in columns:
                print("✅ Column verified: youtube_video_id added successfully")
                return True
            else:
                print("❌ Migration failed: column not found after addition")
                return False
                
        except Exception as e:
            print(f"❌ Migration error: {e}")
            return False

if __name__ == "__main__":
    migrate_database()
