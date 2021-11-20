from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
#https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    business = widgets.CheckboxInput()
    entertainment = widgets.CheckboxInput()
    general = widgets.CheckboxInput()
    health = widgets.CheckboxInput()
    science = widgets.CheckboxInput()
    sports = widgets.CheckboxInput()
    technology = widgets.CheckboxInput()