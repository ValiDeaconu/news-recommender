from flask import Blueprint, render_template, request, session, redirect, url_for

from form.register import Form as RegisterForm
from form.login import Form as LoginForm
from model import User

from hashlib import sha256

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    if session.get('logged_in') == True:
        return render_template('index.html', user=session.get('user'))
    
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
        password = sha256(rf.password.data.encode('utf-8')).hexdigest()

        if rf.validate_on_submit():
            User(username = username, password = password, mutation_rate = 0.0).save()
            return render_template('signup.html', form=rf, success=True, message='Contul a fost creat cu succes.')
            
        return render_template('signup.html', form=rf, success=False)

    return render_template('signup.html', form=rf)

@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('logged_in') == True:
        return redirect(url_for('client.index'))

    lf = LoginForm()

    if request.method == 'POST':
        username = lf.username.data
        password = sha256(lf.password.data.encode('utf-8')).hexdigest()

        if lf.validate_on_submit():
            user = User.find_by_username_and_password(username=username, password=password)

            if user:
                session['logged_in'] = True
                session['user'] = user
                return redirect(url_for('client.index'))
    
            return render_template('signin.html', form=lf, user_does_not_exist=True)

        return render_template('signin.html', form=lf)

    return render_template('signin.html', form=lf)

@blueprint.route('/signout', methods=['GET'])
def signout():
    if session.get('logged_in') == False:
        return redirect(url_for('client.index'))

    session['logged_in'] = False
    session.pop('user')
    return redirect(url_for('client.index'))

@blueprint.route('/categories', methods=['GET'])
def categories():
    return render_template('categories.html')
