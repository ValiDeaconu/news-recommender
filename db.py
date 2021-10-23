from uuid import uuid4, UUID
from sys import stdout, stderr
from server.database.handler import Database
from server.database.types import ReturnCode, RequestType
from server.database.dtos import Request, Response
from server.database.statements import Statements

# Database process
DATABASE_FILE_STORAGE = 'storage.db'


def respond(code: ReturnCode, message: str = '', out: any = None, errs: list[str] = []):
  response = Response(return_code=code, 
                      message=message if message else 'FAIL' if len(errs) > 0 else 'OK', 
                      errors=errs, 
                      data=out if out else None)
  
  print(f'{str(response)}', file=stdout)
  if len(errs) > 0:
    print(f'{errs[0]}', file=stderr)
  else:
    print('', file=stderr)


def process(db: Database, request: Request):
  stmt = request.statement

  if stmt.required_parameters != len(request.params):
    respond(code=ReturnCode.PARAMETERS_COUNT_MISMATCH, 
            errs=[f'This method requires {stmt.required_parameters} parameters. Received {len(request.params)}'])
    return

  exec_params = request.params
  if stmt.generate_pk:
    uuid = uuid4()
    exec_params = tuple(list([uuid.bytes]) + list(exec_params))

  if request.type == RequestType.COMMIT:
    if db.commit(stmt.statement, exec_params):
      respond(code=ReturnCode.SUCCESS, out=str(uuid) if stmt.generate_pk else '')
    else:
      respond(code=ReturnCode.COMMIT_FAILURE, err=['Commit was not applied.'])
  elif request.type == RequestType.EXECUTE:
    if stmt.pk_index >= 0:
      exec_params[stmt.pk_index] = UUID(exec_params[stmt.pk_index]).bytes

    (status, err) = db.execute(stmt.statement, params=exec_params)
    if status:
      respond(code=ReturnCode.SUCCESS)
    else:
      respond(code=ReturnCode.EXECUTE_FAILURE, errs=['Execute was not successful.', err])
  elif request.type == RequestType.QUERY:
    if stmt.pk_index >= 0:
      exec_params[stmt.pk_index] = UUID(exec_params[stmt.pk_index]).bytes
    
    rows = db.query(stmt.statement, params=exec_params)
    
    container = []
    for row in rows:
      decoded_fields = []
      for field in row:
        try:
          decoded_fields.append(str(UUID(bytes=field)))
        except:
          decoded_fields.append(field)
      container.append(dict(list(zip(stmt.fields, tuple(decoded_fields)))))

    respond(code=ReturnCode.SUCCESS, out=container)
  else:
    respond(code=ReturnCode.UNKOWN_COMMAND, errs=['Unkown command.'])

def main():
  db = Database(DATABASE_FILE_STORAGE)
  (status, err) = db.connect()

  if not status:
    respond(code=ReturnCode.CONNECTION_FAILURE, errs=['Could not connect to database', err])
    return

  (status, err) = db.execute(Statements.CREATE_DATABASE.statement)
  if not status:
    respond(code=ReturnCode.EXECUTE_FAILURE, errs=['Could not prepare database', err])
    return

  while True:
    msg = input()

    if msg.startswith('exit'):
      break
    elif msg.startswith('ping'):
      respond(code=ReturnCode.SUCCESS, message='PONG')
    elif msg.startswith('run'):
      [_, json] = msg.split(' ', 1)

      request = Request.build(json)
      process(db, request)

  if not db.close():
    respond(code=ReturnCode.CONNECTION_FAILURE, errs=['Database could not be stopped'])
  else:
    respond(code=ReturnCode.SUCCESS)
  
  return


if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    e_name = e.__class__.__name__
    e_msg = str(e).replace('\n', ' ')
    respond(code=ReturnCode.SOMETHING_WENT_WRONG, errs=['An exception occured', f'{e_name}: {e_msg}'])