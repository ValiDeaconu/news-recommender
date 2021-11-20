from enum import unique
from sqlalchemy.orm import relationship
from model import db

class Locality(db.Model):
    __tablename__ = 'locality'

    id = db.Column(db.Integer, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    name = db.Column(db.String(50), nullable=False, unique=True)
    county = relationship('County', back_populates='localities')

    def __init__(self, county_id: int, name: str):
        self.county_id = county_id
        self.name = name

    @staticmethod
    def find_all_by_county(county_id: int):
        return sorted([(locality.id, locality.name) for locality in Locality.query.filter_by(county_id=county_id).all()], key=lambda i: i[1])