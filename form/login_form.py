from flask_wtf import FlaskForm
from wtforms.fields.simple import TextField

class LoginForm(FlaskForm):
    username = TextField('username')
    password = TextField('password')