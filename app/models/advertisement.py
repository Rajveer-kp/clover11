from app import db
from datetime import datetime

class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    link_url = db.Column(db.String(500))
    ad_type = db.Column(db.String(50), nullable=False)  # banner, sidebar, modal, video
    placement = db.Column(db.String(100), nullable=False)  # dashboard, my-videos, analytics, etc.
    target_role = db.Column(db.String(20))  # creator, editor, or None for all
    
    # Display settings
    background_color = db.Column(db.String(20), default='#667eea')
    text_color = db.Column(db.String(20), default='#ffffff')
    is_active = db.Column(db.Boolean, default=True)
    
    # Scheduling
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    # Analytics
    impressions = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Advertisement {self.title}>'
    
    @property
    def click_through_rate(self):
        """Calculate CTR percentage"""
        if self.impressions == 0:
            return 0.0
        return round((self.clicks / self.impressions) * 100, 2)
    
    def is_currently_active(self):
        """Check if ad should be shown based on schedule and active status"""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        
        # Check start date
        if self.start_date and now < self.start_date:
            return False
            
        # Check end date
        if self.end_date and now > self.end_date:
            return False
            
        return True

class AdClick(db.Model):
    __tablename__ = 'ad_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('advertisements.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    advertisement = db.relationship('Advertisement', backref='click_records')
    user = db.relationship('User', backref='ad_clicks')
    
    def __repr__(self):
        return f'<AdClick {self.id} for Ad {self.ad_id}>'
