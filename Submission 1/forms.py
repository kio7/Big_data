from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], render_kw={"autofocus": True, "placeholder": ""})
    file_url = FileField("Test", validators=[FileRequired(), FileAllowed(["png", "jpg", "mp3", "jepg"])], render_kw={"placeholder": ""})
    submit = SubmitField("Upload file")
