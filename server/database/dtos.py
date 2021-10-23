from json import dumps, loads
from server.database.statements import Statements
from server.database.types import RequestType, ReturnCode

class Request:
  def __init__(self, type: RequestType, statement: Statements.Statement, params: tuple[any]):
    self.type = type
    self.statement = statement
    self.params = params

  def __str__(self):
    return dumps({
      'Type': int(self.type),
      'StatementId': self.statement.id,
      'Parameters': list(self.params)
    })

  @staticmethod
  def build(json: str):
    data = loads(json)
    return Request(RequestType(data['Type']), Statements.get_statement_by_id(data['StatementId']), data['Parameters'])


class Response:
  def __init__(self, return_code: ReturnCode, message: str, errors: list[str], data: any):
    self.return_code = return_code
    self.message = message
    self.errors = errors
    self.data = data

  def __str__(self):
    return dumps({
      'ReturnCode': int(self.return_code),
      'Message': self.message,
      'Errors': self.errors,
      'Data': self.data if self.data else None
    })

  @staticmethod
  def build(json: str):
    data = loads(json)
    return Response(ReturnCode(data['ReturnCode']), data['Message'], data['Errors'], data['Data'])

