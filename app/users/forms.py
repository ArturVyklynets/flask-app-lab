from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from .models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[
    DataRequired(), Length(min=4, max=16),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
    message="Username must start with a letter and contain only letters, numbers, dots or underscores")
  ])

  email = StringField('Email', validators=[
    DataRequired(), Email()
  ])

  password = PasswordField('Password', validators=[
    DataRequired(), Length(min=6)
  ])

  confirm_password = PasswordField('Confirm Password', validators=[
    DataRequired(), EqualTo('password')
  ])

  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email is already registered.')
    
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()]) 
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
  username = StringField('Username', validators=[
    DataRequired(), Length(min=4, max=16),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
    message="Username must start with a letter and contain only letters, numbers, dots or underscores")
  ])

  email = StringField('Email', validators=[
    DataRequired(), Email()
  ])

  old_password = PasswordField('Old Password')
  new_password = PasswordField('New Password')
  confirm_password = PasswordField('Confirm Password', validators=[
    EqualTo('new_password',  message="Confirm Password must match New Password")
  ])
  image_file = FileField('Update Account Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
  about_me = TextAreaField('About Me', validators=[
        Length(max=500, message="About Me cannot exceed 500 characters.")
    ])

  last_seen = StringField('Last Seen', render_kw={'readonly': True})
  submit = SubmitField('Update')