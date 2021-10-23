from flask import jsonify, make_response
from server import database

class Response:
  def __init__(self, status: int, message: str = '', errors: list[str] = [], data: any = None):
    self.status = status
    self.message = message
    self.errors = errors
    self.data = data

  def __str__(self):
    return jsonify({
      'Status': self.status,
      'Message': self.message,
      'Errors': self.errors,
      'Data': self.data
    })

  def as_http_response(self):
    return make_response(self.__str__(), self.status)

  @staticmethod
  def from_database_response(db_response: database.dtos.Response):
    return Response(status=200 if db_response.return_code == database.types.ReturnCode.SUCCESS else 500,
                    message=db_response.message,
                    errors=db_response.errors,
                    data=db_response.data)