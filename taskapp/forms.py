from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from taskapp import db_connection

cursor = db_connection.cursor()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # check if user with the same username exists
    def validate_username(self, username):
        cursor.execute(""" SELECT * FROM Users WHERE Username = %s """, (username.data,))
        user = cursor.fetchall()
        if user:
            raise ValidationError('Username is taken. please choose a different one')

    # check if user with the same email exists
    def validate_email(self, email):
        cursor.execute(""" SELECT * FROM Users WHERE Email = %s """, (email.data,))
        user = cursor.fetchall()
        if user:
            raise ValidationError('Email is taken. please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateTimeField('Due Date', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Done')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateTimeField('Due Date', format='%Y-%m-%dT%H:%M')
    description = StringField('Description')
    submit = SubmitField('Done')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateTimeField('Date and Time', format='%Y-%m-%dT%H:%M')
    description = StringField('Description')
    submit = SubmitField('Done')

