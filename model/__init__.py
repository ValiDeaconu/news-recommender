from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from model.user import User
from model.user_category import UserCategory
from model.user_keyword import UserKeyword