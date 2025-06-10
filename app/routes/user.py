from flask import Blueprint, render_template, redirect
from ..forms import RegistrationForm
from ..extensions import db
from ..models.user import User

user = Blueprint('user', __name__)

@user.route('/user/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.name.data)
        print(form.pas.data)
        print(form.avatar.data)
        return redirect('/')
    else:
        print("[INFO]: Ошибка регистрации!")

    return render_template('user/register.html', form=form)