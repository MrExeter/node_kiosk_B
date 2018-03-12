import os
from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app.movie import main
from app.movie.models import Movie
from app.movie.forms import CreateMovieForm, EditMovieForm


@main.route('/')
def display_movies():
    return redirect(url_for('authentication.do_the_login'))


@main.route('/movies')
@login_required
def movie_list():
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

    if request.method == 'POST':
        db.session.delete(movie)
        db.session.commit()
        flash('movie deleted successfully')
        return redirect(url_for('main.movie_list'))

    return render_template('delete_movie.html', movie=movie, movie_id=movie_id)


@main.route('/movie/edit/<movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get(movie_id)

    # session["current_address"] = movie.network_address  # temp store movie ip address in session
    form = EditMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.name = form.name.data
        movie.location = form.location.data
        db.session.add(movie)
        db.session.commit()
        flash('movie updated successfully')
        return redirect(url_for('main.movie_list'))

    return render_template('edit_movie.html', form=form)


@main.route('/create/movie', methods=['GET', 'POST'])
@login_required
def create_movie():

    form = CreateMovieForm()

    if form.validate_on_submit():

        Movie.create_movie(
            name=form.name.data,
            location=form.location.data
        )
        flash('Registration Successful')
        return redirect(url_for('main.movie_list'))

    return render_template('create_movie.html', form=form)


@main.route('/upload')
@login_required
def upload():
    return render_template('upload_movie.html')


@main.route('/uploader', methods=['GET', 'POST'])
@login_required
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        # f.save(secure_filename(f.filename))
        app_path = os.getcwd()
        the_path = app_path + UPLOAD_FOLDER + '/'
        # f.save(the_path, filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'file uploaded successfully'

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @main.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(main.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#
#         return render_template('upload_movie.html')
