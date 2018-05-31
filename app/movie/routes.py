'''
Description - Routes for kiosk movie model
@author - John Sentz
@date - 10-Apr-2018
@time - 10:33 AM
'''

import os

from sqlalchemy.exc import IntegrityError, DatabaseError, DataError
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, UPLOAD_FOLDER
from app.movie import main
from app.movie.forms import CreateMovieForm, CreatePlaylistForm, EditPlaylistForm
from app.movie.models import Movie, Playlist
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


@main.route('/playlists')
@login_required
def playlist_list():
    playlists = Playlist.query.all()

    return render_template('playlist_list.html', playlists=playlists)


@main.route('/create/playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = CreatePlaylistForm()
    if form.validate_on_submit():

        Playlist.create_playlist(form.name.data, form.movies.data)
        flash('Playlist Creation Successful')
        return redirect(url_for('main.playlist_list'))

    return render_template('create_playlist.html', form=form)


@main.route('/playlist/detail/<playlist_id>')
@login_required
def playlist_detail(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    movies = []
    for movie in playlist.playlists:
        movies.append(movie)
    return render_template('playlist_detail.html', playlist=playlist, movies=movies)


@main.route('/playlist/edit/<playlist_id>', methods=['GET', 'POST'])
@login_required
def edit_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    form = EditPlaylistForm(obj=playlist)

    if form.validate_on_submit():
        # kiosk.network_address = form.network_address.data
        # kiosk.location = form.location.data
        playlist.name = form.name.data
        playlist.movies = form.movies.data

        try:
            db.session.add(playlist)
            db.session.commit()
            flash('Playlist updated successfully')
            return redirect(url_for('main.playlist_list'))

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")

    return render_template('edit_playlist.html', form=form)


@main.route('/playlist/delete/<playlist_id>', methods=['GET', 'POST'])
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)

    if request.method == 'POST':

        db.session.delete(playlist)
        db.session.commit()
        flash('Playlist deleted successfully')
        return redirect(url_for('main.playlist_list'))

    return render_template('delete_playlist.html', playlist=playlist, playlist_id=playlist_id)


@main.route('/system_stats')
# @login_required
def get_system_stats():
    system_monitor = SystemMonitor()
    return system_monitor.get_system_stats()


@main.route('/loop_video/')
# @login_required
def loop_video():

    movie_id = request.args.get('movie_id')
    BobUecker.loop_video(movie_id)

    return ''


@main.route('/stop_loop_video/')
# @login_required
def stop_loop_video():

    BobUecker.all_not_playing()
    BobUecker.stop_video()
    return ''
