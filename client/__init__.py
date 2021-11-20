from flask import Blueprint, render_template, request, session, redirect, url_for

from form.register import Form as RegisterForm
from form.login import Form as LoginForm
from form.profile import Form as ProfileForm
from model import User, UserKeyword

from hashlib import sha256
import requests
import json
import datetime

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))
    
    keywords = UserKeyword.find_all_liked_by_user_id(session.get("user").id)

    url = 'https://newsapi.org/v2/everything?sortBy=popularity&apiKey=a29ea4304a564e7bbf8275c596a64dd1&q='

    if len(keywords) >= 1:
        query = ' OR '.join([k for k in keywords])
    else:
        query = 'a'

    url = f'{url}{query}'

    print(url)

    response = requests.get(url)

    articles = response.json()['articles']

    for a in articles:
        a['publishedAt'] = datetime.datetime.strptime(a['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %B %Y %H:%M')

    return render_template('index.html', news=articles)

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
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.index'))

    session['logged_in'] = False
    session.pop('user')
    return redirect(url_for('client.index'))

@blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.index'))

    user = User.find_by_id(session.get('user').id)

    pf = ProfileForm()

    if request.method == 'GET':
        pf.mutation_rate.data = int(user.mutation_rate * 100.0)

    if request.method == 'POST':
        print (pf.mutation_rate.data)
        mutation_rate = pf.mutation_rate.data

        if pf.validate_on_submit():
            user.mutation_rate = mutation_rate / 100.0
            user.save()

            return render_template('profile.html', 
                                    form=pf, 
                                    user=session.get('user'),
                                    success=True, 
                                    message=f'Rata de mutație a fost actualizată la {mutation_rate}.')

    return render_template('profile.html', form=pf, user=session.get('user'))

@blueprint.route('/categories', methods=['GET'])
def categories():
    return render_template('categories.html')
