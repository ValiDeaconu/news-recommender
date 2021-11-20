from flask import Blueprint, send_file, jsonify
from os.path import join

from model import MovieOnDay, Locality, Reservation


mbp = Blueprint('movie', __name__)
lbp = Blueprint('locality', __name__)
dbp = Blueprint('download', __name__)
rbp = Blueprint('reservation', __name__)

Blueprints = [
    ('/movie', mbp),
    ('/locality', lbp),
    ('/download', dbp),
    ('/reservation', rbp),
]

@lbp.route('/<county_id>', methods=['GET'])
def find_localities_in_county(county_id):
    localities = Locality.query.filter_by(county_id=county_id).all()

    return jsonify([{'id': l.id, 'name': l.name} for l in localities])


@mbp.route('/<activity_day_id>', methods=['GET'])
def find_movies_on_day(activity_day_id):
    mods = MovieOnDay.query.filter_by(activity_day_id=activity_day_id).all()

    return jsonify([{'id': mod.id, 'name': f'{mod.movie.name} [{mod.movie.genre.name}] @{mod.hour}'} for mod in mods])


@dbp.route('/invoices/<invoice_name>')
def download_invoice(invoice_name):
    invoice_path = join('download', 'invoices', invoice_name)

    return send_file(invoice_path, mimetype='pdf', as_attachment=True)


@dbp.route('/xmls/<xml_doc_name>')
def download_reservation(xml_doc_name):
    xml_doc_path = join('download', 'xmls', xml_doc_name)

    return send_file(xml_doc_path, mimetype='xml', as_attachment=True)

@rbp.route('/all', methods=['GET'])
def get_all_reservations():
    reservations = Reservation.query.all()

    return jsonify([{
        'id': r.id,
        'owner': r.owner,
        'movie': r.on_day.movie.name,
        'locality': r.locality.name,
        'county': r.locality.county.name,
        'row': r.row,
        'column': r.column,
        'day': r.on_day.activity_day.name,
        'hour': r.on_day.hour
    } for r in reservations])