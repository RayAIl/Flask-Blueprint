from ..extensions import db

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250)) # Длинна темы