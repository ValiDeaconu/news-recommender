from flask import Blueprint, render_template
from server.controllers.response import Response

index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/')
def home():
  return render_template('index.html', title='Hei', username='Ana')

@index_bp.route('/status')
def status():
  return Response(status=200, message='All systems are OK!').as_http_response()
