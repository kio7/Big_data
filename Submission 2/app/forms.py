import os
from flask_wtf import FlaskForm

from wtforms import SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import NumberRange

class FileForm(FlaskForm):
    folder_choices = [
        (folder, folder)
        for folder in os.listdir(os.path.join(os.path.dirname(__file__), "static/photos/clustering"))
        if os.path.isdir(os.path.join(os.path.dirname(__file__), f"static/photos/clustering/{folder}"))
    ]
    folder = SelectField("Select a dataset", choices=folder_choices)
    clusters = SelectField(
        "Select no. of clusters",
        choices=[(2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8")],
        coerce=int,
        default=3,
    )
    show_filenames = BooleanField("Show filenames?")
    submit = SubmitField("Select")


class ChoosePictureForm(FlaskForm):
    picture_choices = [
        (picture, picture)
        for picture in os.listdir(os.path.join(os.path.dirname(__file__), "static/photos/segmentation"))
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"static/photos/segmentation/{picture}"))
    ]
    picture = SelectField("Select a picture", choices=picture_choices)
    threshold = IntegerField("Threshold", validators=[NumberRange(min=0)])
    submit = SubmitField("Select")
