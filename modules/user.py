from datetime import datetime, timedelta
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        ret = check_password_hash(self.password_hash, password)
        if ret:
            self.failed_attempts = 0
            self.locked_until = None
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 5:
                self.locked_until = datetime.now() + timedelta(minutes=1)
                self.failed_attempts = 0
        self.save_db()

        return ret

    @classmethod
    def get_user(cls, username):
        return cls.query.filter_by(username=username).first()

    def save_db(self):
        db.session.add(self)
        db.session.commit()

    def check_lock(self):
        if self.locked_until and self.locked_until > datetime.now():
            return True
        return False
