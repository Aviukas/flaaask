from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(min=1, max=80)])
    submit = SubmitField('Create Group')

class BillForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=120)])
    amount = FloatField('Amount', validators=[DataRequired()])
    payer_id = IntegerField('Payer ID', validators=[DataRequired()])
    submit = SubmitField('Add Bill')
