from sqlalchemy.orm import relationship
from model import db

class MovieOnDay(db.Model):
    __tablename__ = 'movie_on_day'

    id = db.Column(db.Integer, primary_key=True)
    activity_day_id = db.Column(db.Integer, db.ForeignKey('activity_day.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    hour = db.Column(db.String(5), nullable=False, default='00:00')

    activity_day = relationship('ActivityDay', back_populates='movies')
    movie = relationship('Movie', back_populates='on_days')

    def __init__(self, activity_day_id: int, movie_id: int, hour: str):
        self.activity_day_id = activity_day_id
        self.movie_id = movie_id
        self.hour = hour

    def __str__(self):
        return f'{self.movie.name} [{self.movie.genre.name}] @{self.hour}'

    @staticmethod
    def find_all_by_day(activity_day_id: int):
        return [(mod.id, str(mod)) for mod in MovieOnDay.query.filter_by(activity_day_id=activity_day_id).all()]