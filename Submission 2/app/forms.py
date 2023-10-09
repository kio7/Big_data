import os
from flask_wtf import FlaskForm

from wtforms import SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import NumberRange


class FileForm(FlaskForm):
    clusters = SelectField(
        "Select no. of clusters",
        choices=[(2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8")],
        coerce=int,
        default=3,
    )
    show_filenames = BooleanField("Show filenames?")
    submit = SubmitField("Select")


class ChoosePictureForm(FlaskForm):
    threshold = IntegerField("Threshold", validators=[NumberRange(min=0)])
    submit = SubmitField("Select")


class DICOMImageForm(FlaskForm):
    picture_choices = [
        (picture, picture)
        for picture in os.listdir(os.path.join(os.path.dirname(__file__), "static/images/Dicom"))
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"static//images/Dicom/{picture}"))
    ]
    picture = SelectField("Select a picture", choices=picture_choices)
    submit = SubmitField("Select")


