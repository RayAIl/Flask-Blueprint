from ..extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from .post import Topic

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='user')
    name = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    login = db.Column(db.String(50))
    pas = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship(Topic, backref='author')