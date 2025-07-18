from datetime import datetime
from ..extensions import db
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    subject = db.Column(db.String(250))
    student = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.utcnow)