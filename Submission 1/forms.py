import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    # title = StringField("Title", validators=[DataRequired()], render_kw={"autofocus": True, "placeholder": ""})
    
    folder_choices = [(folder, folder) for folder in os.listdir('static/photos/clustering') if os.path.isdir(os.path.join('static/photos/clustering', folder))]
    folder = SelectField("Select a dataset", choices=folder_choices)
    clusters = SelectField(
        "Select no. of clusters", 
        choices=[(2, "2"),(3, "3"),(4, "4"),(5, "5"),(6, "6"),(7, "7"),(8, "8")], # (value, tekst)
        default=3,
        coerce=int)
    submit = SubmitField("Select")


