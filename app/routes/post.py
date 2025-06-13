from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from ..extensions import db
from ..models.post import Topic

post = Blueprint('post', __name__)

@post.route('/', methods=['POST', 'GET'])
def all():
    posts = Topic.query.order_by(Topic.data).all()
    return render_template('post/all.html', posts=posts)

@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        teacher = request.form.get('teacher')
        student = request.form.get('student')
        subject = request.form.get('subject')
        
        post = Topic(teacher=teacher, subject=subject, student=student)
        
        try:
            db.session.add(post)
            db.session.commit()
            print("[INFO]: В базу данных успешно внесена информация! ")
            return redirect('/')

        except Exception as ex:
            print(f"[ERROR]: Возникла ошибка при добовлении в базу данных: {str(ex)}")
            
    else:
        return render_template('post/create.html')

@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):

    post = Topic.query.get(id)

    if request.method == 'POST':
        post.teacher = request.form.get('teacher')
        post.subject = request.form.get('student')
        post.student = request.form.get('subject')

        try:
            db.session.commit()
            return redirect('/')
        
        except Exception as ex:
            print(f"[ERROR]: Возникла ошибка: {str(ex)}")

    else:
        return render_template('post/update.html', post=post)

@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):

    post = Topic.query.get(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')    
    
    except Exception as ex:
        print(f"[ERROR]: Возникла ошибка: {str(ex)}")