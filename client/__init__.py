from flask import Blueprint, render_template, request

from form.register import Form as RegisterForm
from model import User

from passlib.hash import sha256_crypt

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

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    rf = RegisterForm()

    if request.method == 'POST':
        username = rf.username.data
        password = rf.password.data

        if rf.validate_on_submit():
            User(username = username, password = sha256_crypt.hash(password), mutation_rate = 0.0).save()
            return render_template('signup.html', form=rf, success=True, message='Contul a fost creat cu succes.')
            
        return render_template('signup.html', form=rf, success=False, message='Error.')

    return render_template('signup.html', form=rf)

@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@blueprint.route('/categories', methods=['GET'])
def categories():
    return render_template('categories.html')
