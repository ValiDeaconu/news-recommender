from flask import Blueprint, send_file, jsonify, request, session, make_response
from os.path import join
from passlib.hash import sha256_crypt

from model import User, UserCategory, UserKeyword

from form.register import Form as RegisterForm
from form.login import Form as LoginForm
from form.set_categories import Form as SetCategoriesForm

ubp = Blueprint('user', __name__)
cbp = Blueprint('category', __name__)
kbp = Blueprint('keyword', __name__)

Blueprints = [
    ('/user', ubp),
    ('/user_category', cbp)
]

# Register
@ubp.route('/register', methods=["POST"])
def add_guide():
    form = RegisterForm()

    if form.password.data != form.confirm_password.data:
        return -1

    User(username = form.username.data, password = sha256_crypt.hash(form.password.data), mutation_rate = 0.0).save()

# Login
@ubp.route('/login', methods=["POST"])
def login():
    form = LoginForm()

    user = User.find_by_username_and_password(username = form.username.data)
    if not user :
        return -1

    session['user'] = user
    return 0

# Set user categories
@cbp.route('/', methods=["POST"])
def set_user_categories():
    form = SetCategoriesForm()

    return 0

# Set user mutation rate
@ubp.route('/mutation/<mutation_rate>', methods=["POST"])
def set_user_mutation_rate(mutation_rate):
    current_user = session.get('user')

    current_user.mutation_rate = mutation_rate
    current_user.save()

    return 0

# Get news api

# Get headlines by category

# Set liked user keywords
@kbp.route('/liked', methods=["POST"])
def set_liked_user_keywords():
    user_id = session.get('user').id
    keywords = request.json['keywords']

    for keyword in keywords:
        UserKeyword(user_id = user_id, keyword = keyword, liked = True).save()

    return 0

# Set disliked user keywords
@kbp.route('/disliked', methods=["POST"])
def set_disliked_user_keywords():
    user_id = get_current_user().id
    keywords = request.json['keywords']

    for keyword in keywords:
        UserKeyword(user_id = user_id, keyword = keyword, liked = False).save()

    return 0



# @lbp.route('/<county_id>', methods=['GET'])
# def find_localities_in_county(county_id):
#     localities = Locality.query.filter_by(county_id=county_id).all()

#     return jsonify([{'id': l.id, 'name': l.name} for l in localities])


# @mbp.route('/<activity_day_id>', methods=['GET'])
# def find_movies_on_day(activity_day_id):
#     mods = MovieOnDay.query.filter_by(activity_day_id=activity_day_id).all()

#     return jsonify([{'id': mod.id, 'name': f'{mod.movie.name} [{mod.movie.genre.name}] @{mod.hour}'} for mod in mods])


# @mbp.route('/<activity_day_id>', methods=['GET'])
# def find_movies_on_day(activity_day_id):
#     mods = MovieOnDay.query.filter_by(activity_day_id=activity_day_id).all()

#     return jsonify([{'id': mod.id, 'name': f'{mod.movie.name} [{mod.movie.genre.name}] @{mod.hour}'} for mod in mods])




# @dbp.route('/invoices/<invoice_name>')
# def download_invoice(invoice_name):
#     invoice_path = join('download', 'invoices', invoice_name)

#     return send_file(invoice_path, mimetype='pdf', as_attachment=True)


# @dbp.route('/xmls/<xml_doc_name>')
# def download_reservation(xml_doc_name):
#     xml_doc_path = join('download', 'xmls', xml_doc_name)

#     return send_file(xml_doc_path, mimetype='xml', as_attachment=True)

# @rbp.route('/all', methods=['GET'])
# def get_all_reservations():
#     reservations = Reservation.query.all()

#     return jsonify([{
#         'id': r.id,
#         'owner': r.owner,
#         'movie': r.on_day.movie.name,
#         'locality': r.locality.name,
#         'county': r.locality.county.name,
#         'row': r.row,
#         'column': r.column,
#         'day': r.on_day.activity_day.name,
#         'hour': r.on_day.hour
#     } for r in reservations])