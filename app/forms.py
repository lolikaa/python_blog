from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ta nazwa użytkownika jest już zajęta. Wybierz inną nazwę.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten e-mail jest już zarejestrowany')


class LoginForm(FlaskForm):
    username = StringField("Login",
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Hasło',
                             validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class PostForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    body = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Dodaj post')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Zaktualizuj')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ten login jest zajęty. Proszę wybierz inny login')

    def validate_email(self, email):
        if email.data != current_user.username:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ten e-mail jest już zarejestrowany w bazie')

