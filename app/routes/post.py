from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user

from ..forms import StudentForm, TeacherForm
from ..extensions import db
from ..models.post import Topic
from ..models.user import User

post = Blueprint('post', __name__)

@post.route('/', methods=['POST', 'GET'])
def all():
    form = TeacherForm()
    form.teacher.choices = [teach.name for teach in User.query.filter_by(status='teacher')]

    if request.method == "POST":
        teacher = request.form.get('teacher')
        teacher_id = User.query.filter_by(name=teacher).first().id
        posts = Topic.query.filter_by(teacher=teacher_id).order_by(Topic.data.desc()).all()
    else:
        posts = Topic.query.order_by(Topic.data.desc()).limit(70).all()

    return render_template('post/all.html', posts=posts, user=User, form=form)

@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = StudentForm()
    form.student.choices = [stud.name for stud in User.query.filter_by(status='user')]
    if request.method == 'POST':
        student = request.form.get('student')
        student_id = User.query.filter_by(name=student).first().id
        subject = request.form.get('subject')
        
        post = Topic(teacher=current_user.id, subject=subject, student=student_id)
        
        try:
            db.session.add(post)
            db.session.commit()
            print("[INFO]: В базу данных успешно внесена информация! ")
            return redirect('/')

        except Exception as ex:
            print(f"[ERROR]: Возникла ошибка при добовлении в базу данных: {str(ex)}")
            
    else:
        return render_template('post/create.html', form=form)

@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Topic.query.get(id)

    if post.author.id == current_user.id:
        form = StudentForm()
        form.student.data = User.query.filter_by(id=post.student).first().name
        form.student.choices = [stud.name for stud in User.query.filter_by(status='user')]

        if request.method == 'POST':
            post.subject = request.form.get('subject')
            student = request.form.get('student')

            post.student = User.query.filter_by(name=student).first().name

            try:
                db.session.commit()
                return redirect('/')
        
            except Exception as ex:
                print(f"[ERROR]: Возникла ошибка: {str(ex)}")

        else:
            return render_template('post/update.html', post=post, form=form)
    else:
        abort(403)

@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):

    post = Topic.query.get(id)

    if post.author.id == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')    
    
        except Exception as ex:
            print(f"[ERROR]: Возникла ошибка: {str(ex)}")
    else:
        abort(403)