from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bop.models import User

#create class, specify the fields and its validators
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #custom validation with self and username as a argument
    def validate_username(self, username):
        #query wheter username being submited to the form is already in database
        user = User.query.filter_by(username=username.data).first()
        #if user exists
        if user:
            #throw error validation message
            raise ValidationError('That username is taken. please choose a different one')


    #custom validation with self and username as a argument
    def validate_email(self, email):
        #query wheter email being submited to the form is already in database
        user = User.query.filter_by(email=email.data).first()
        #if user with that email exists
        if user:
            #throw error validation message
            raise ValidationError('That email is taken. Please choose a different one')
                                                        
class LoginForm(FlaskForm):                             
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')              
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        #if username isn't equal to current username
        if username.data != current_user.username:
            #then run these validation checks
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. please choose a different one')



    def validate_email(self, email):
        #if email isn't equal to current email
        if email.data != current_user.email:
            #then run these validation checks
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
      
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
