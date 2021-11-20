from sqlalchemy.orm import relationship
from model import db

class ActivityDay(db.Model):
    __tablename__ = 'activity_day'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    movies = relationship('MovieOnDay')

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def find_all():
        return [(day.id, day.name) for day in ActivityDay.query.all()]