from subprocess import Popen, PIPE
from time import sleep
from server.database.types import ReturnCode, RequestType
from server.database.statements import Statements
from server.database.dtos import Response, Request

# TODO: Find a better approach
OPEN_DB_SHELL = ['python', 'db.py']

class Api:
  def __init__(self):
    self._p = Popen(OPEN_DB_SHELL, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf8', bufsize=1, universal_newlines=True)  

  def _read_output(self):
    while not self._p.stdout.readable() or not self._p.stderr.readable():
      sleep(0.1) # wait for 100ms
      
    out = self._p.stdout.readline()[:-1] # get rid of the newline
    err = self._p.stderr.readline()[:-1] # get rid of the newline

    response = Response.build(out) if out else Response(ReturnCode.UNKNOWN_OUTPUT, 
                                                        '', 
                                                        ['Could not extract output', err], 
                                                        None)
               
    return response

  def _communicate(self, message: str):
    try:
      self._p.stdin.write(f'{message}\n')
    except BrokenPipeError as e:
      return Response(return_code=ReturnCode.COMMUNICATION_FAILURE, 
                      errors=['Could not communicate with database', 'BrokenPipe', str(e)])
    except Exception as e:
      return Response(return_code=ReturnCode.COMMUNICATION_FAILURE, 
                      errors=['Something went wrong', e.__class__.__name__, str(e).split('\n').join(' ')])

    return self._read_output()

  def is_connected(self):
    if not self._p.poll():
      response = self._communicate('ping')
      return response.return_code == ReturnCode.SUCCESS and response.message == 'PONG'
  
    return False

  def close(self):
    code, out, err = self._communicate('exit')
    self._p.kill()
    
    return code, out, err

  def execute(self, request_type: RequestType, statement: Statements.Statement, params: tuple[any]):
    req = Request(request_type, statement, params)

    return self._communicate(f'run {str(req)}')