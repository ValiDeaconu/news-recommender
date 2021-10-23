class Statements:
  class Statement:
    def __init__(self, 
                id: int,
                generate_pk: bool,
                pk_index: int,
                required_parameters: int,
                statement: str,
                fields: str = ''):
      self.id = id
      self.generate_pk = generate_pk
      self.pk_index = pk_index
      self.required_parameters = required_parameters
      self.statement = statement
      self.fields = fields

  # Constants
  _USER_TABLE_NAME  = 'users'

  # Statements
  CREATE_DATABASE = Statement(id=0, 
                              generate_pk=False, 
                              pk_index=-1,
                              required_parameters=0, 
                              statement=f"""CREATE TABLE IF NOT EXISTS {_USER_TABLE_NAME} (
                                id BINARY(16) PRIMARY KEY,
                                username VARCHAR(45) NOT NULL DEFAULT '',
                                password UNSIGNED BIT INT NOT NULL DEFAULT 0
                              );""")

  INSERT_USER = Statement(id=1, 
                          generate_pk=True, 
                          pk_index=0, 
                          required_parameters=2, 
                          statement=f'INSERT INTO {_USER_TABLE_NAME} (id, username, password) VALUES (?, ?, ?)')
  
  SELECT_USER = Statement(id=2, 
                          generate_pk=False, 
                          pk_index=0, 
                          required_parameters=1, 
                          statement=f'SELECT * FROM {_USER_TABLE_NAME} WHERE id = ?',
                          fields=('id', 'username', 'password'))

  SELECT_ALL_USERS = Statement(id=3, 
                               generate_pk=False, 
                               pk_index=-1, 
                               required_parameters=0,
                               statement=f'SELECT * FROM {_USER_TABLE_NAME}',
                               fields=('id', 'username', 'password'))

  DELETE_USER = Statement(id=4,
                          generate_pk=False,
                          pk_index=0,
                          required_parameters=1,
                          statement=f'DELETE FROM {_USER_TABLE_NAME} WHERE id = ?')

  @staticmethod
  def get_statement_by_id(id: int):
    return {
      0: Statements.CREATE_DATABASE,
      1: Statements.INSERT_USER,
      2: Statements.SELECT_USER,
      3: Statements.SELECT_ALL_USERS,
      4: Statements.DELETE_USER
    }[id]
