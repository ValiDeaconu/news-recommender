from sqlalchemy.orm import relationship
from model import db

class County(db.Model):
    __tablename__ = 'county'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    auto = db.Column(db.String(2), nullable=False, unique=True)
    localities = relationship('Locality')

    def __init__(self, name, auto):
        self.name = name
        self.auto = auto

    @staticmethod
    def find_all():
        return sorted([(county.id, county.name) for county in County.query.all()], key=lambda i: i[1])
