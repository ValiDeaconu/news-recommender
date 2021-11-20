from flask_wtf import FlaskForm
from wtforms import BooleanField

class Form(FlaskForm):
    business = BooleanField(false_values=(False, 'false', ''))
    entertainment = BooleanField(false_values=(False, 'false', ''))
    health = BooleanField(false_values=(False, 'false', ''))
    science = BooleanField(false_values=(False, 'false', ''))
    sports = BooleanField(false_values=(False, 'false', ''))
    technology = BooleanField(false_values=(False, 'false', ''))