'''
Description - Movie Model
@author - John Sentz
@date - 09-Mar-2018
@time - 2:24 PM
'''


from app import db


class Movie(db.Model):

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file_name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    play_count = db.Column(db.Integer)
    currently_playing = db.Column(db.Boolean, nullable=False)

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
        return 'Video name : {}, File : {}, Play count = {}'.format(self.name, self.file_name, self.play_count)
