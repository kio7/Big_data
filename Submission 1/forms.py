import os
from flask_wtf import FlaskForm

from wtforms import SubmitField, SelectField, BooleanField


class FileForm(FlaskForm):
    folder_choices = [
        (folder, folder)
        for folder in os.listdir(os.path.join(os.path.dirname(__file__), "static/photos/clustering"))
        if os.path.isdir(os.path.join(os.path.dirname(__file__), f"static/photos/clustering/{folder}"))
    ]
    folder = SelectField("Select a dataset", choices=folder_choices)
    show_filenames = BooleanField("Show filenames?")
    submit = SubmitField("Select")


class ChoosePictureForm(FlaskForm):
    picture_choices = [
        (picture, picture)
        for picture in os.listdir(os.path.join(os.path.dirname(__file__), "static/photos/segmentation"))
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"static/photos/segmentation/{picture}"))
    ]
    picture = SelectField("Select a picture", choices=picture_choices)
    submit = SubmitField("Select")
