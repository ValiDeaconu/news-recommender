from flask import Blueprint
from server.controllers.response import Response

error_handler_bp = Blueprint('errorhandler', __name__)

@error_handler_bp.errorhandler(Exception)
def handle_exception(e):
    response = Response(status=500,
                        message=e.name,
                        errors=[e.description])

    return response.as_http_response()