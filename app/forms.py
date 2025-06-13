from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from .models.user import User

class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=6, max=20)])
    login = StringField('Логин', validators=[DataRequired(), Length(min=6, max=20)])
    pas = PasswordField('Пароль', validators=[DataRequired()])
    conf_pas = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('pas')])
    avatar = FileField('Загрузите аватарку', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Зарегистрироваться')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError("[INFO]: Имя данного пользователя уже занято. Пожалуйста, выберите другое...")

class LoginForm(FlaskForm):
    """Form to log users"""
    login = StringField('Логин', validators=[DataRequired(), Length(min=6, max=20)])
    pas = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')