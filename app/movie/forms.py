'''
Description - Kiosk movie create form class
@author - John Sentz
@date - 10-Apr-2018
@time - 10:35 AM
'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError

from app.movie.models import Movie


def filename_exists(form, field):
    f = form.video.data
    filename = secure_filename(f.filename)
    movie = Movie.query.filter_by(file_name=filename).first()
    if movie:
        raise ValidationError('Duplicate filename already exists')


def name_exists(form, field):
    movie = Movie.query.filter_by(name=field.data).first()
    if movie:
        raise ValidationError('Duplicate movie name already exists')


class CreateMovieForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           name_exists])
    video = FileField(validators=[FileRequired(), filename_exists])
    submit = SubmitField('Create')
