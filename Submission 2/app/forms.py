import os
from flask_wtf import FlaskForm

from wtforms import SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import NumberRange


class PatterRecognitionForm(FlaskForm):
    picture_choices = sorted([
        (picture, picture)
        for picture in os.listdir(os.path.join(os.path.dirname(__file__), "static/pr_images"))
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"static/pr_images/{picture}"))
    ])
    picture = SelectField("Select a picture", choices=picture_choices)
    submit = SubmitField("Select")


class DICOMImageForm(FlaskForm):
    picture_choices = [
        (picture, picture)
        for picture in os.listdir(os.path.join(os.path.dirname(__file__), "static/images/Dicom"))
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"static//images/Dicom/{picture}"))
    ]
    picture = SelectField("Select a picture", choices=picture_choices)
    submit = SubmitField("Select")


