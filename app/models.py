from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class RiverHeight(db.Model):
    """
    Model for storing river height data.
    Database: kalugangadb
    """
    __tablename__ = 'river_heights'
    __bind_key__ = 'kalugangadb'
    
    id = db.Column(db.Integer, primary_key=True)
    river_name = db.Column(db.String(100), nullable=False, default='Kalu Ganga (Ratnapura)', index=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    height = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Colombo')))
    
    def __repr__(self):
        return f'<RiverHeight {self.river_name} {self.timestamp}: {self.height}m>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'river_name': self.river_name,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'height': self.height,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def get_kalu_ganga_data(cls, limit=100, start_date=None, end_date=None):
        """
        Get river height data specifically for Kalu Ganga.
        
        Args:
            limit (int): Maximum number of records to return
            start_date (datetime): Start date for filtering (inclusive)
            end_date (datetime): End date for filtering (inclusive)
        
        Returns:
            list: List of RiverHeight objects for Kalu Ganga only
        """
        query = cls.query.filter(cls.river_name == 'Kalu Ganga (Ratnapura)')
        
        if start_date:
            query = query.filter(cls.timestamp >= start_date)
        if end_date:
            query = query.filter(cls.timestamp <= end_date)
        
        return query.order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_latest_kalu_ganga_height(cls):
        """
        Get the most recent Kalu Ganga river height record.
        
        Returns:
            RiverHeight: Latest Kalu Ganga record or None if no records exist
        """
        return cls.query.filter(
            cls.river_name == 'Kalu Ganga (Ratnapura)'
        ).order_by(cls.timestamp.desc()).first()
    
    @classmethod
    def get_kalu_ganga_last_24h(cls):
        """
        Get Kalu Ganga river height records from the last 24 hours.
        
        Returns:
            list: List of RiverHeight objects for Kalu Ganga from last 24 hours
        """
        from datetime import timedelta
        now = datetime.now(pytz.timezone('Asia/Colombo'))
        start_time = now - timedelta(hours=24)
        
        return cls.query.filter(
            cls.river_name == 'Kalu Ganga (Ratnapura)',
            cls.timestamp >= start_time
        ).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def get_kalu_ganga_last_7days(cls):
        """
        Get Kalu Ganga river height records from the last 7 days.
        
        Returns:
            list: List of RiverHeight objects for Kalu Ganga from last 7 days
        """
        from datetime import timedelta
        now = datetime.now(pytz.timezone('Asia/Colombo'))
        start_time = now - timedelta(days=7)
        
        return cls.query.filter(
            cls.river_name == 'Kalu Ganga (Ratnapura)',
            cls.timestamp >= start_time
        ).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def get_kalu_ganga_statistics(cls):
        """
        Get basic statistics for Kalu Ganga river height data.
        
        Returns:
            dict: Statistics including count, min, max, average, latest
        """
        records = cls.query.filter(cls.river_name == 'Kalu Ganga (Ratnapura)').all()
        
        if not records:
            return {
                'count': 0,
                'min_height': 0,
                'max_height': 0,
                'avg_height': 0,
                'latest_height': 0,
                'latest_timestamp': None
            }
        
        heights = [record.height for record in records]
        latest = records[-1] if records else None
        
        return {
            'count': len(records),
            'min_height': min(heights),
            'max_height': max(heights),
            'avg_height': sum(heights) / len(heights),
            'latest_height': latest.height if latest else 0,
            'latest_timestamp': latest.timestamp if latest else None
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
