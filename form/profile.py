from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerRangeField
from wtforms.validators import DataRequired, NumberRange
FIELD_REQUIRED_TPL = 'Campul "{}" este obligatoriu.'
MINIMUM_LENGTH_TPL = 'Campul "{}" trebuie sa contina minim {} caractere.'

class Form(FlaskForm):
    mutation_rate = IntegerRangeField('mutation_rate', validators=[
        NumberRange(min=1, max=100, message='Valorea ratei de mutație trebuie să fie între 1 și 100.')
    ])