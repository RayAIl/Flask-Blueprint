from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=6, max=20)])
    login = StringField('Логин', validators=[DataRequired(), Length(min=6, max=20)])
    pas = PasswordField('Пароль', validators=[DataRequired()])
    conf_pas = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('pas')])
    avatar = FileField('Загрузите аватарку', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Зарегистрироваться')