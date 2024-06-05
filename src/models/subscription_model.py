from src import db

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    type = db.Column(db.String(10))
    renewal_type = db.Column(db.String(10))
    subscription_id = db.Column(db.String(50))
    next_payment_date = db.Column(db.Date)
    quota_usage = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='subscriptions')