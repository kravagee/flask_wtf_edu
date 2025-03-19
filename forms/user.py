from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    id_astr = StringField('ID астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    id_cap = StringField('ID капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class LoginForm(FlaskForm):
    id_astr = StringField('ID')
    password = PasswordField('Пароль', validators=[DataRequired()])
    id_cap = StringField('ID капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')