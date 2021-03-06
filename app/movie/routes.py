'''
Description - Routes for kiosk movie model
@author - John Sentz
@date - 10-Apr-2018
@time - 10:33 AM
'''

import os

from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, UPLOAD_FOLDER
from app.movie import main
from app.movie.forms import CreateMovieForm, CreatePlaylistForm, EditPlaylistForm
from app.movie.models import Movie, Playlist
from app.utils.link_controller import LinkController
from app.utils.utils import SystemMonitor, BobUecker


@main.route('/')
def display_movies():
    return redirect(url_for('authentication.do_the_login'))


@main.route('/movies')
@login_required
def movie_list():
    """Display all movies currently available on the node"""
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)


# @main.route('/remote/movies')
# @login_required
# def remote_movie_list():
#     movies = Movie.query.all()
#     return render_template('movie_list.html', movies=movies)


@main.route('/movie/detail/<movie_id>')
@login_required
def movie_detail(movie_id):
    """
    Displays movie details base on an ID
    :param movie_id:
    :return: Renders movie detail template for given movie
    """
    movie = Movie.query.get(movie_id)
    return render_template('movie_detail.html', movie=movie)


@main.route('/movie/delete/<movie_id>', methods=['GET', 'POST'])
@login_required
def delete_movie(movie_id):
    """
    Deletes a movie based on an id, Will ask for a confirmation first.
    :param movie_id:
    :return:
    """
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
    """
    Displays form for creating and uploading a movie object.
    The user enters a name and is provided a file upload widget.
    :return:
    """
    form = CreateMovieForm()

    if form.validate_on_submit():
        f = form.video.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))

        Movie.create_movie(
            name=form.name.data,
            file_name=filename,
            location=os.path.join(UPLOAD_FOLDER, filename)
        )
        return redirect(url_for('main.movie_list'))

    return render_template('create_movie.html', form=form)


@main.route('/playlists')
@login_required
def playlist_list():
    """Displays available playlists"""
    playlists = Playlist.query.all()

    return render_template('playlist_list.html', playlists=playlists)


@main.route('/create/playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    """
    Create playlist.
    The user enters a name, selects videos for playlist and has the option to \
    set video for play on boot.
    :return:
    """
    form = CreatePlaylistForm()
    if form.validate_on_submit():

        Playlist.create_playlist(form.name.data, form.play_on_start.data, form.movies.data)
        return redirect(url_for('main.playlist_list'))

    return render_template('create_playlist.html', form=form)


@main.route('/playlist/detail/<playlist_id>')
@login_required
def playlist_detail(playlist_id):
    """Display playlist details given an ID"""
    playlist = Playlist.query.get(playlist_id)
    links = playlist.links
    movies = []
    for link in links:
        movie = Movie.query.get(link.movie_id)
        movies.append(movie)

    return render_template('playlist_detail.html', playlist=playlist, movies=movies)


@main.route('/playlist/edit/<playlist_id>', methods=['GET', 'POST'])
@login_required
def edit_playlist(playlist_id):
    """Edit playlist given an ID"""
    playlist = Playlist.query.get(playlist_id)
    session["current_playlist_name"] = playlist.name    # Save playlist name prior to editing

    links = playlist.links

    form = EditPlaylistForm(obj=playlist)
    if request.method == 'GET':
        form.play_on_start = playlist.play_on_start
        if playlist.links:
            # if there are links, then retrieve the movies that they link to
            links = playlist.links
            movies = [Movie.query.get(link.movie_id) for link in links]
            form.movies.data = [movie for movie in movies]

    if form.validate_on_submit():
        # Update name and movie list of playlist
        # playlist.play_on_start = form.play_on_start.data
        playlist.update_playlist(form.name.data, form.play_on_start.data, form.movies.data)
        return redirect(url_for('main.playlist_list'))

    return render_template('edit_playlist.html', form=form)


@main.route('/playlist/delete/<playlist_id>', methods=['GET', 'POST'])
@login_required
def delete_playlist(playlist_id):
    """Delete a playlist based on its ID, confirmation is required"""
    playlist = Playlist.query.get(playlist_id)
    directory_name = playlist.directory_name
    if request.method == 'POST':

        db.session.delete(playlist)
        db.session.commit()
        linkcontroller = LinkController()
        linkcontroller.delete_links(directory_name)
        linkcontroller.delete_playlist_directory(directory_name)
        flash('Playlist deleted successfully')
        return redirect(url_for('main.playlist_list'))

    return render_template('delete_playlist.html', playlist=playlist, playlist_id=playlist_id)


@main.route('/system_stats')
# @login_required
def get_system_stats():
    """Returns JSON object containing system stats"""
    system_monitor = SystemMonitor()
    return system_monitor.get_system_stats()


@main.route('/receive_scheduler', methods=['GET', 'POST'])
def receive_scheduler():
    schedule_data = request.get_json()
    if schedule_data == '' or schedule_data is None:
        return "False"
    else:
        return "True"
# @main.route('/play_video_once/')
# def play_video_once():
#
#     movie_id = request.args.get('movie_id')
#     player = BobUecker.play_single(movie_id)
#     session["the_omxplayer"] = player
#     return ''


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


@main.route('/loop_playlist/')
def loop_playlist():
    playlist_id = request.args.get('playlist_id')
    BobUecker.loop_playlist(playlist_id)
    return 'loop playlist'


@main.route('/stop_loop_playlist/')
def stop_loop_playlist():
    BobUecker.all_not_playing()
    BobUecker.stop_video()
    return 'stop loop playlist'


@main.route('/sleep_kiosk_display/')
def sleep_kiosk_display():
    BobUecker.sleep_display()
    return 'sleep kiosk display'


@main.route('/wake_kiosk_display/')
def wake_kiosk_display():
    BobUecker.wake_display()

    # Check for any playlist set to play on wake
    playlist = Playlist.query.filter_by(play_on_start=True).first()
    if playlist:
        # # Construct payload to package with request
        # payload = {"playlist_id": playlist.id}
        # requests.get('http://0.0.0.0:5100/loop_playlist', params=payload)
        BobUecker.loop_playlist(playlist.id)

    return 'wake kiosk display'
