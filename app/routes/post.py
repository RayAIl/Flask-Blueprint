from flask import Blueprint
from ..extensions import db
from ..models.post import Topic

post = Blueprint('post', __name__)

@post.route('/post/<subject>')
def create_subject(subject):
    post = Topic(subject=subject)
    db.session.add(post)
    db.session.commit()
    return 'Subject Created!'