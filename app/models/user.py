from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))  # optional full name
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='creator')  # 'editor', 'creator', or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Account creation timestamp
    
    # YouTube OAuth credentials
    youtube_credentials = db.Column(db.Text)  # JSON string of credentials
    youtube_channel_name = db.Column(db.String(200))  # Channel name for display
    youtube_connected = db.Column(db.Boolean, default=False)  # Quick connection status check

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_youtube_credentials(self, credentials_dict):
        """Store YouTube credentials as JSON string."""
        self.youtube_credentials = json.dumps(credentials_dict)
        self.youtube_connected = True

    def get_youtube_credentials(self):
        """Retrieve YouTube credentials as dictionary."""
        if self.youtube_credentials:
            return json.loads(self.youtube_credentials)
        return None

    def disconnect_youtube(self):
        """Remove YouTube credentials."""
        self.youtube_credentials = None
        self.youtube_channel_name = None
        self.youtube_connected = False

    def __repr__(self):
        return f'<User {self.email} - Role: {self.role}>'
