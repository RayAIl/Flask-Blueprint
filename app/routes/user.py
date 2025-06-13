from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user

from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User
from ..functions import save_picture

user = Blueprint('user', __name__)

@user.route('/user/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pas = bcrypt.generate_password_hash(form.pas.data).decode("UTF-8")
        avatar_filename = save_picture(form.avatar.data)
        user = User(name=form.name.data, login=form.login.data, avatar=avatar_filename, pas=hashed_pas)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"[INFO]: Регистрация {form.login.data} выполнена успешно!", "success")
            return redirect(url_for('user.login'))
        except Exception as ex:
            flash(f"[INFO]: Ошибка регистрации! {str(ex)}", "danger")
    return render_template('user/register.html', form=form)

@user.route('/user/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        new_user = User.query.filter_by(login=form.login.data).first()
        if new_user and bcrypt.check_password_hash(new_user.pas, form.pas.data):
            login_user(new_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"[INFO]: Вход {form.login.data} выполнен успешно!", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash('[INFO]: Ошибка входа! Пожалуйста проверьте логин и пароль!', 'danger')
    return render_template('user/login.html', form=form)

@user.route('/user/login', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))