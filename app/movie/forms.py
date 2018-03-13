

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError
import re

from app.movie.models import Movie

#
# def network_address_exists(form, field):
#     kiosk = Kiosk.query.filter_by(network_address=field.data).first()
#     network_address = kiosk.network_address
#
#     if network_address == temp_address:
#         session["current_address"] = ''
#         return True
#
#     if kiosk:
#         raise ValidationError('IP address already in use')
#
#
# def network_address_valid(form, field):
#     # Check to see if IP address is in valid form e.g., ###.###.###.### where each ### is 255 or less
#     valid_ip_pattern = re.compile(
#         "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
#     test = valid_ip_pattern.match(field.data)
#     if not test:
#         raise ValidationError('Invalid IP address format')


class CreateMovieForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    video = FileField(validators=[FileRequired()])
    # location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditMovieForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    # location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update')


