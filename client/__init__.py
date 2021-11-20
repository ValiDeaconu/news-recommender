from flask import Blueprint, request, session, redirect, url_for, render_template

from form.register import Form as RegisterForm
from form.login import Form as LoginForm
from form.profile import Form as ProfileForm
from form.categories import Form as CategoryForm

from model import User, UserCategory

from news import get_news_for_user

from hashlib import sha256
from datetime import datetime

blueprint = Blueprint('client', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))

    user = User.find_by_id(id=session.get("user_id"))
    news = get_news_for_user(user_id=user.id)

    # Add id to articles and change date to human readable format
    id = 0
    for article in news:
        article['publishedAt'] = datetime.strptime(
            article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %B %Y %H:%M')
        article['id'] = id
        id += 1

    return render_template('index.html', news=news, user=user)


@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('logged_in') == True:
        return redirect(url_for('client.index'))

    lf = LoginForm()

    if request.method == 'POST':
        username = lf.username.data
        password = sha256(lf.password.data.encode('utf-8')).hexdigest()

        if lf.validate_on_submit():
            user = User.find_by_username_and_password(
                username=username, password=password)

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


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    rf = RegisterForm()

    if request.method == 'POST':
        username = rf.username.data
        password = sha256(rf.password.data.encode('utf-8')).hexdigest()

        if rf.validate_on_submit():
            user = User(username=username, password=password,
                        mutation_rate=0.5)
            user.save()
            session['logged_in'] = True
            session['user_id'] = user.id
            session['fresh_account'] = True
            return redirect(url_for('client.setup'))

        return render_template('signup.html', form=rf, success=False)

    return render_template('signup.html', form=rf)


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

        print(categories)
        user_id = session.get('user_id')

        for category in categories:
            UserCategory(user_id=user_id, category=category).save()

        session.pop('fresh_account')

        return redirect(url_for('client.index'))

    return render_template('categories.html', form=cf)


@blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in') or session.get('logged_in') == False:
        return redirect(url_for('client.signin'))

    user = User.find_by_id(session.get('user_id'))

    pf = ProfileForm()

    if request.method == 'GET':
        pf.mutation_rate.data = int(user.mutation_rate * 100.0)

    if request.method == 'POST':
        mutation_rate = pf.mutation_rate.data

        if pf.validate_on_submit():
            user.mutation_rate = mutation_rate / 100.0
            user.save()

            return render_template('profile.html',
                                   form=pf,
                                   user=User.find_by_id(
                                       id=session.get('user_id')),
                                   success=True,
                                   message=f'Rata de mutație a fost actualizată la {mutation_rate}.')

    return render_template('profile.html', form=pf, user=User.find_by_id(id=session.get('user_id')))
