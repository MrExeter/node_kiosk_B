'''
Description - Movie Model
@author - John Sentz
@date - 09-Mar-2018
@time - 2:24 PM
'''
from flask import flash
from sqlalchemy.exc import IntegrityError, DatabaseError, DataError
from sqlalchemy.orm.exc import FlushError

from app import db
from app.utils.link_controller import LinkController

link_playlists = db.Table('link_playlists',
                          db.Column('link_id', db.Integer, db.ForeignKey('videolink.id'), primary_key=True),
                          db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
                          )


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file_name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    play_count = db.Column(db.Integer)
    currently_playing = db.Column(db.Boolean, nullable=False, default=False)
    play_on_start = db.Column(db.Boolean, nullable=False, default=False)
    links = db.relationship('VideoLink',
                            foreign_keys="[VideoLink.movie_id, VideoLink.full_filepath]",
                            cascade="all",
                            backref='movie',
                            lazy=True)

    @classmethod
    def create_movie(cls, name, file_name, location):
        movie = cls(name=name,
                    file_name=file_name,
                    location=location)

        try:
            db.session.add(movie)
            db.session.commit()
            flash("Movie created successfully")
            return movie

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")
            flash("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")
            flash("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")
            flash("Database Error encountered")

    def __init__(self, name, file_name, location, play_count=0, currently_playing=False):
        self.name = name
        self.file_name = file_name
        self.location = location
        self.play_count = play_count
        self.currently_playing = currently_playing

    def __repr__(self):
        return 'Video name : {}, File : {}'.format(self.name, self.file_name)


class VideoLink(db.Model):
    __tablename__ = 'videolink'

    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(32), nullable=False)
    full_filepath = db.Column(db.String(128), nullable=False, unique=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    linkplaylist = db.relationship('Playlist',
                                   secondary=link_playlists,
                                   lazy='subquery',
                                   single_parent=True,
                                   backref=db.backref('links', cascade="all", lazy=True))

    def __init__(self, movie, link_path):
        self.movie_name = movie.name
        self.full_filepath = link_path
        self.movie_id = movie.id

    @classmethod
    def create_link(cls, movie):
        videolink = cls(movie=movie)

        try:
            db.session.add(videolink)
            db.session.commit()
            return videolink

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")


PLAYLIST_ROOT = "/home/pi/node_kiosk_B/app/static/videos/playlists/"


class Playlist(db.Model):
    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    directory_path = db.Column(db.String(128))
    directory_name = db.Column(db.String(64))
    currently_playing = db.Column(db.Boolean, nullable=False, default=False)
    play_on_start = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name
        self.directory_name = self.name.replace(" ", "")

    def get_directory_name(self):
        return self.directory_name

    def set_name(self, name):
        self.name = name
        self.directory_name = self.name.replace(" ", "")

    def set_directory_path(self, directory_path):
        self.directory_path = directory_path

    def get_directory_path(self):
        return self.directory_path

    @classmethod
    def get_playlist_path(cls, playlist_name):
        return PLAYLIST_ROOT + playlist_name + "/"

    @classmethod
    def create_playlist(cls, name, *movies):
        playlist = cls(name)
        directory = playlist.directory_name

        # Root of all playlist directories
        playlist_root_directory = PLAYLIST_ROOT + directory + "/"
        playlist.set_directory_path(playlist_root_directory)

        # List that will be used to pass tuples of (movie, link)
        movie_link_pairs = []

        try:
            db.session.add(playlist)
            db.session.commit()

            linkz = []
            movies = movies[0]  # convert tuple to list
            for movie in movies:
                link_path = playlist_root_directory + str(movies.index(movie)) + ".mp4"
                video_link = VideoLink(movie=movie, link_path=link_path)

                # List of tuples (movie, link) used to create links on disk
                movie_link_pairs.append((movie, video_link))

                db.session.add(video_link)
                db.session.commit()
                linkz.append(video_link)

            for link in linkz:
                playlist.links.append(link)
            db.session.commit()

            # Create playlist directory and symlinks
            create_linkcontroller = LinkController()
            create_linkcontroller.create_playlist_directory(playlist_root_directory)
            create_linkcontroller.create_links(directory, *movie_link_pairs)

            flash('Playlist Creation Successful')
            return 'Playlist Creation Successful'

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")
            flash("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")
            flash("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")
            flash("Database Error encountered")

        except FlushError:
            db.session.rollback()
            print("Database Flush Error encountered")
            flash("Database Flush Error encountered")

    def __repr__(self):
        return "Playlist : {}".format(self.name)

    def update_playlist(self, new_name, *new_movies):

        # directory = new_name.replace(" ", "")
        # playlist_root_directory = PLAYLIST_ROOT + directory + "/"

        # list of tuples (movie, link)
        movie_link_pairs = []

        try:
            if self.name != new_name:
                # Name Change!
                # Complete change, playlist name changes, create new playlist directory and populate with links
                old_name = self.name
                old_directory_name = self.directory_name
                self.set_name(new_name)
                db.session.commit()

                # Retrieve old links for deletion
                old_links = self.links
                for old_link in old_links:
                    db.session.delete(old_link)
                    db.session.commit()

                linkz = []

                playlist_root_directory = PLAYLIST_ROOT + self.directory_name + "/"
                self.set_directory_path(playlist_root_directory)

                new_movies = new_movies[0]  # convert tuple to list
                for movie in new_movies:
                    link_path = playlist_root_directory + str(new_movies.index(movie)) + ".mp4"
                    video_link = VideoLink(movie=movie, link_path=link_path)

                    db.session.add(video_link)
                    db.session.commit()
                    linkz.append(video_link)

                    movie_link_pairs.append((movie, video_link))

                for link in linkz:
                    self.links.append(link)
                db.session.commit()

                # Delete old links and old playlist directory
                delete_linkcontroller = LinkController()
                delete_linkcontroller.delete_links(old_directory_name)
                delete_linkcontroller.delete_playlist_directory(old_directory_name)

                # Create new playlist directory and populate with new links
                create_linkcontroller = LinkController()
                create_linkcontroller.create_playlist_directory(playlist_root_directory)
                create_linkcontroller.create_links(self.directory_name, *movie_link_pairs)

                flash('Playlist Updated Successful')

            else:
                # Path doesn't change, just delete links that are now dead, save those that are valid
                old_links = self.links
                for old_link in old_links:
                    db.session.delete(old_link)
                    db.session.commit()

                linkz = []

                playlist_root_directory = PLAYLIST_ROOT + self.directory_name + "/"

                new_movies = new_movies[0]  # convert tuple to list
                for movie in new_movies:
                    link_path = playlist_root_directory + str(new_movies.index(movie)) + ".mp4"
                    video_link = VideoLink(movie=movie, link_path=link_path)

                    db.session.add(video_link)
                    db.session.commit()
                    linkz.append(video_link)

                    movie_link_pairs.append((movie, video_link))

                for link in linkz:
                    self.links.append(link)
                db.session.commit()

                # Delete old links and create new links disk
                update_linkcontroller = LinkController()
                update_linkcontroller.delete_links(self.directory_name)
                update_linkcontroller.create_links(self.directory_name, *movie_link_pairs)

                flash('Playlist Updated Successful')

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")
            flash("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")
            flash("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")
            flash("Database Error encountered")

        except FlushError:
            db.session.rollback()
            print("Database Flush Error encountered")
            flash("Database Flush Error encountered")
