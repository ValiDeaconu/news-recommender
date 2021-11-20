from flask import Blueprint, render_template, request

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')