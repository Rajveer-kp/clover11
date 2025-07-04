from app import db
from datetime import datetime

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[creator_id], backref='sent_invitations')
    editor = db.relationship('User', foreign_keys=[editor_id], backref='received_invitations')
    
    def __repr__(self):
        return f'<Invitation {self.id}: {self.creator.name} -> {self.editor.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'editor_id': self.editor_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'creator_name': self.creator.name,
            'editor_name': self.editor.name
        }
