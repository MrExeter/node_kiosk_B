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
    name = db.Column(db.String(64), nullable=False, index=True)
    location = db.Column(db.String(128), nullable=False)
    play_count = db.Column(db.Integer)

    @classmethod
    def create_movie(cls, name, location):
        movie = cls(name=name,
                    location=location)

        db.session.add(movie)
        db.session.commit()
        return movie

    def __init__(self, name, location, play_count=0):
        self.name = name
        self.location = location
        self.play_count = play_count

    def __repr__(self):
        return 'Video name : {}, Play count = {}'.format(self.name, self.play_count)
