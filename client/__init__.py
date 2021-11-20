from flask import Blueprint, render_template, request, session, redirect, url_for

from form.register import Form as RegisterForm
from form.login import Form as LoginForm
from form.profile import Form as ProfileForm
from form.categories import Form as CategoryForm
from model import User, UserKeyword, UserCategory

from hashlib import sha256
import requests
import json
import datetime

blueprint = Blueprint('client', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))
    
    keywords = UserKeyword.find_all_liked_by_user_id(user_id=session.get("user_id"))

    url = 'https://newsapi.org/v2/everything?sortBy=popularity&apiKey=a29ea4304a564e7bbf8275c596a64dd1&q='

    if len(keywords) >= 1:
        query = ' OR '.join([k for k in keywords])
    else:
        query = 'a'

    url = f'{url}{query}'

    response = requests.get(url)

    articles = response.json()['articles']

    for a in articles:
        a['publishedAt'] = datetime.datetime.strptime(a['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %B %Y %H:%M')

    return render_template('index.html', news=articles, user=User.find_by_id(id=session.get("user_id")))

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
            user = User(username = username, password = password, mutation_rate = 50.0)
            user.save()
            session['logged_in'] = True
            session['user_id'] = user.id
            session['fresh_account'] = True
            return redirect(url_for('client.setup'))

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
                session['user_id'] = user.id
                return redirect(url_for('client.index'))
    
            return render_template('signin.html', form=lf, user_does_not_exist=True)

        return render_template('signin.html', form=lf)

    return render_template('signin.html', form=lf)

@blueprint.route('/signout', methods=['GET'])
def signout():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))

    session['logged_in'] = False
    session.pop('user')
    return redirect(url_for('client.signin'))

@blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))

    user = User.find_by_id(session.get('user_id'))

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
                                    user=User.find_by_id(id=session.get('user_id')),
                                    success=True, 
                                    message=f'Rata de mutație a fost actualizată la {mutation_rate}.')

    return render_template('profile.html', form=pf, user=User.find_by_id(id=session.get('user_id')))

@blueprint.route('/setup', methods=['GET', 'POST'])
def setup():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))
        
    if not session.get('fresh_account') or session.get('fresh_account') == False:
        return redirect(url_for('client.index'))

    cf = CategoryForm()

    if request.method == 'POST':
        # Set 'general' as default for each user so there's no need to
        # extra check if no category is selected
        categories = ['general']
        
        if cf.business.data:
            categories.append('business')

        if cf.entertainment.data:
            categories.append('entertainment')
        
        if cf.health.data:
            categories.append('health')
            
        if cf.science.data:
            categories.append('science')
            
        if cf.sports.data:
            categories.append('sports')
            
        if cf.technology.data:
            categories.append('technology')

        print (categories)
        user_id = session.get('user_id')

        for category in categories:
            UserCategory(user_id=user_id, category=category).save()

        session.pop('fresh_account')

        return redirect(url_for('client.index'))

    return render_template('categories.html', form=cf)
