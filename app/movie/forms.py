'''
Description - Kiosk movie create form class
@author - John Sentz
@date - 10-Apr-2018
@time - 10:35 AM
'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, FileField, SelectField
# from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from flask_admin.form.widgets import Select2Widget

# from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import ModelForm, QuerySelectField, QuerySelectMultipleField

from app.movie.models import Movie, Playlist


def filename_exists(form, field):
    f = form.video.data
    filename = secure_filename(f.filename)
    movie = Movie.query.filter_by(file_name=filename).first()
    if movie:
        raise ValidationError('Duplicate filename already exists')


def movie_name_exists(form, field):
    movie = Movie.query.filter_by(name=field.data).first()
    if movie:
        raise ValidationError('Duplicate movie name already exists')


def playlist_name_exists(form, field):
    playlist = Playlist.query.filter_by(name=field.data).first()
    if playlist:
        raise ValidationError('Duplicate playlist name already exists')


class CreateMovieForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           movie_name_exists])
    video = FileField(validators=[FileRequired(), filename_exists])
    submit = SubmitField('Create')


def movie_query():
    return Movie.query


class CreatePlaylistForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(),
                                           playlist_name_exists])

    movies = QuerySelectMultipleField(u'Videos',
                                      query_factory=lambda: Movie.query.all(),
                                      allow_blank=True,
                                      blank_text=u'',
                                      get_label='name')

    submit = SubmitField('Create Playlist')


class EditPlaylistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           playlist_name_exists])

    movies = QuerySelectMultipleField(u'Videos',
                                      query_factory=lambda: Movie.query.all(),
                                      allow_blank=True,
                                      blank_text=u'',
                                      get_label='name')

    submit = SubmitField('Update Playlist')



