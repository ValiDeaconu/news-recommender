from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from model.activity_day import ActivityDay
from model.county import County
from model.genre import Genre
from model.locality import Locality
from model.movie_on_day import MovieOnDay
from model.movie import Movie
from model.reservation import Reservation
