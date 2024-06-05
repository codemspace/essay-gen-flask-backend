from src import db

class Social_account(db.Model):
    __tablename__ = 'social_accounts'
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    provider = db.Column(db.String(10)) # Google
    uid = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='social_accounts')