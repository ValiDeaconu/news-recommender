from flask import Blueprint, render_template, request

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@blueprint.route('/generic', methods=['GET'])
def generic():
    return render_template('generic.html')

@blueprint.route('/elements', methods=['GET'])
def elements():
    return render_template('elements.html')

@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('login.html')