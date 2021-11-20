from flask import Blueprint, render_template, request
from werkzeug.utils import send_from_directory
from os import path

from model import County, ActivityDay, MovieOnDay, Locality, Reservation

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')