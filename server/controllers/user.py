import uuid
from flask import request, Blueprint

from server import db_api
from server import database
from server.controllers.response import Response

user_bp = Blueprint('user', __name__)

@user_bp.route("/user/<string:id>", methods=["GET"])
def user_get(id: str):
    user_id = uuid.UUID(id)

    if not db_api.is_connected():
        return 'Could not establish connection with database', 500
    
    db_response = db_api.execute(database.types.RequestType.QUERY, database.statements.Statements.SELECT_USER, params=(str(user_id), ))
    return Response.from_database_response(db_response).as_http_response()

@user_bp.route("/user", methods=["GET"])
def user_get_all():
    if not db_api.is_connected():
        return 'Could not establish connection with database', 500
    
    db_response = db_api.execute(database.types.RequestType.QUERY, database.statements.Statements.SELECT_ALL_USERS, params=())
    return Response.from_database_response(db_response).as_http_response()


@user_bp.route("/user", methods=['POST'])
def user_create():
    body = request.json

    username = body['Username']
    password = body['Password']

    if not db_api.is_connected():
        return 'Could not establish connection with database', 500
    
    db_response = db_api.execute(database.types.RequestType.COMMIT, database.statements.Statements.INSERT_USER, params=(username, password))
    return Response.from_database_response(db_response).as_http_response()


@user_bp.route("/user/<string:id>", methods=["DELETE"])
def user_delete(id: str):
    user_id = uuid.UUID(id)

    if not db_api.is_connected():
        return 'Could not establish connection with database', 500
    
    db_response = db_api.execute(database.types.RequestType.EXECUTE, database.statements.Statements.DELETE_USER, params=(str(user_id), ))
    return Response.from_database_response(db_response).as_http_response()
