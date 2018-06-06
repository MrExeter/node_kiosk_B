'''
Description - Movie Model
@author - John Sentz
@date - 09-Mar-2018
@time - 2:24 PM
'''


from app import db
from sqlalchemy.exc import IntegrityError, DatabaseError, DataError

movie_playlists = db.Table('movie_playlists',
                           db.Column('movie_id', db.Integer, db.ForeignKey('movie.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
                           db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
                           )
# movie_playlists = db.Table('movie_playlists',
#                            db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
#                            db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
#                            )


class Movie(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file_name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    play_count = db.Column(db.Integer)
    currently_playing = db.Column(db.Boolean, nullable=False)
    movieplaylist = db.relationship('Playlist', secondary=movie_playlists,
                                    backref=db.backref('playlists', lazy='dynamic'))

    @classmethod
    def create_movie(cls, name, file_name, location):
        movie = cls(name=name,
                    file_name=file_name,
                    location=location)

        db.session.add(movie)
        db.session.commit()
        return movie

    def __init__(self, name, file_name, location, play_count=0, currently_playing=False):
        self.name = name
        self.file_name = file_name
        self.location = location
        self.play_count = play_count
        self.currently_playing = currently_playing

    def __repr__(self):
        return 'Video name : {}, File : {}'.format(self.name, self.file_name)


class Playlist(db.Model):

    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_playlist(cls, name, *movies):
        playlist = cls(name)
        try:
            db.session.add(playlist)
            # db.session.commit()
            for movie in movies:
                playlist.playlists.extend(movie)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            print("Database Integrity Error encountered")

        except DataError:
            db.session.rollback()
            print("Data Error encountered")

        except DatabaseError:
            db.session.rollback()
            print("Database Error encountered")

    # @classmethod
    # def update_playlist(cls, name, *movies):
    #     playlist = cls(name)
    #     try:
    #         db.session.add(playlist.name)
    #         db.session.commit()
    #
    #         # clear existing relationships
    #         movie_playlists.query().filter_by(playlist.id).delete()
    #
    #         for movie in movies:
    #             playlist.playlists.extend(movie)
    #
    #         db.session.commit()
    #
    #     except IntegrityError:
    #         db.session.rollback()
    #         print("Database Integrity Error encountered")
    #
    #     except DataError:
    #         db.session.rollback()
    #         print("Data Error encountered")
    #
    #     except DatabaseError:
    #         db.session.rollback()
    #         print("Database Error encountered")

    def __repr__(self):
        return "Playlist : {}".format(self.name)
