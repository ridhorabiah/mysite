from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from mysite.models import User, Application
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')


class ApplicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired(), Length(max=20)])
    platform = StringField('Platform', validators=[DataRequired(), Length(max=30)])
    database = StringField('Database', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Post')

    def validate_name(self, name):
        app = Application.query.filter_by(name=name.data).first()
        if app:
            raise ValidationError('That name is taken. Please choose a different one.')
