from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
#https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class Form(FlaskForm):
      multi = MultiCheckboxField('Multibox', choices=[(1, 'business'),
                                                        (2, 'entertainment'), 
                                                        (3, 'general'), 
                                                        (4, 'health'), 
                                                        (5, 'science'),
                                                        (6, 'sports'), 
                                                        (7, 'technology')], coerce=int)
