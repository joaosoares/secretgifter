from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    name = db.Column(db.String(50), index = True)
    pw_hash = db.Column(db.String(260))
    credits = db.Column(db.Integer)
    draws = db.relationship('Draw', backref = 'creator', lazy = 'dynamic')


    def __init__(self, email, password, name):
        self.email = email
        self.name = name
        self.set_password(password)
        self.credits = 0;

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    

class Draw(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.String(10))