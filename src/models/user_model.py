from src import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    firstname = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    email = db.Column(db.String(70), unique = True)
    avatar = db.Column(db.String(100))
    password = db.Column(db.String(80))