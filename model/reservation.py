from sqlalchemy.orm import relationship
from model import db

class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(50), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    movie_on_day_id = db.Column(db.Integer, db.ForeignKey('movie_on_day.id'))
    locality_id = db.Column(db.Integer, db.ForeignKey('locality.id'))
    

    locality = relationship('Locality')
    on_day = relationship('MovieOnDay')

    def __init__(self, owner: str, row: int, column: int, movie_on_day_id: int, locality_id: int):
        self.owner = owner
        self.row = row
        self.column = column
        self.movie_on_day_id = movie_on_day_id
        self.locality_id = locality_id

    def save(self):
        db.session.add(self)
        db.session.commit()