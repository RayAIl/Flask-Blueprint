from datetime import datetime
from ..extensions import db
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(250))
    subject = db.Column(db.String(250))
    student = db.Column(db.String(250))
    data = db.Column(db.DateTime, default=datetime.utcnow)