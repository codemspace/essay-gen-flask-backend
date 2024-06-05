from src import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    title = db.Column(db.String(100))
    available_sentences = db.Column(db.Integer)
    content = db.Column(db.JSON)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='documents')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)