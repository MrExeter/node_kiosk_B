import os
from flask import render_template, flash, request, redirect, url_for, jsonify, logging
from flask_login import login_required
from omxplayer.player import OMXPlayer
from werkzeug.utils import secure_filename

import time

from app import db, UPLOAD_FOLDER
from app.movie import main
from app.movie.models import Movie
from app.movie.forms import CreateMovieForm
from app.utils.utils import SystemMonitor, BobUecker


@main.route('/')
def display_movies():
    return redirect(url_for('authentication.do_the_login'))


@main.route('/movies')
@login_required
def movie_list():
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)


@main.route('/remote/movies')
@login_required
def remote_movie_list():
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)


@main.route('/movie/detail/<movie_id>')
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('movie_detail.html', movie=movie)


@main.route('/movie/delete/<movie_id>', methods=['GET', 'POST'])
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    filename = movie.file_name

    if request.method == 'POST':
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        db.session.delete(movie)
        db.session.commit()
        flash('movie deleted successfully')
        return redirect(url_for('main.movie_list'))

    return render_template('delete_movie.html', movie=movie, movie_id=movie_id)


# @main.route('/movie/edit/<movie_id>', methods=['GET', 'POST'])
# @login_required
# def edit_movie(movie_id):
#     movie = Movie.query.get(movie_id)
#     existing_filename = movie.file_name
#     # session["current_address"] = movie.network_address  # temp store movie ip address in session
#     form = EditMovieForm(obj=movie)
#
#     if form.validate_on_submit():
#         f = form.video.data
#         new_filename = secure_filename(f.filename)
#         movie.name = form.name.data
#
#         if new_filename != existing_filename:
#             os.remove(os.path.join(UPLOAD_FOLDER, existing_filename))
#             f.save(os.path.join(UPLOAD_FOLDER, new_filename))
#             movie.file_name = new_filename
#
#         else:
#             f.save(os.path.join(UPLOAD_FOLDER, existing_filename))
#             movie.file_name = existing_filename
#
#         db.session.add(movie)
#         db.session.commit()
#         flash('movie updated successfully')
#         return redirect(url_for('main.movie_list'))
#
#     return render_template('edit_movie.html', form=form)


@main.route('/create/movie', methods=['GET', 'POST'])
@login_required
def create_movie():

    form = CreateMovieForm()

    if form.validate_on_submit():
        # f = request.files['file']
        f = form.video.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))

        Movie.create_movie(
            name=form.name.data,
            file_name=filename,
            location=os.path.join(UPLOAD_FOLDER, filename)
        )
        flash('Movie Created Successful')
        return redirect(url_for('main.movie_list'))

    return render_template('create_movie.html', form=form)


@main.route('/system_stats')
# @login_required
def get_system_stats():
    system_monitor = SystemMonitor()
    return system_monitor.get_system_stats()


@main.route('/video')
def play_video():
    VIDEO_1_PATH = "app/static/videos/test_video.mp4"
    player_log = logging.getLogger("Player 1")

    player = OMXPlayer(VIDEO_1_PATH,
                       dbus_name='org.mpris.MediaPlayer2.omxplayer1')
    player.set_aspect_mode('stretch')
    time.sleep(15)
    player.quit()

    return ''


@main.route('/loop_video/')
# @login_required
def loop_video():
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)
    full_file_path = movie.location
    BobUecker.loop_video(full_file_path)
    return ''


@main.route('/stop_loop_video/')
# @login_required
def stop_loop_video():
    BobUecker.stop_video()
    return ''

# @main.route('/upload')
# @login_required
# def upload():
#     return render_template('upload_movie.html')
#
#
# @main.route('/uploader', methods=['GET', 'POST'])
# @login_required
# def uploader():
#     if request.method == 'POST':
#         f = request.files['file']
#         filename = secure_filename(f.filename)
#         f.save(os.path.join(UPLOAD_FOLDER, filename))
#         return 'file uploaded successfully'
