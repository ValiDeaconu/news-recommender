import sqlite3
from server.database.types import QueryType
  
class Database:
  def __init__(self, database_file: str) -> None:
      self._handle = None
      self._db_file_path = database_file

  def connect(self) -> tuple[bool, str]:
    self._handle = None
    try:
      self._handle = sqlite3.connect(database=self._db_file_path)
    except sqlite3.Error as e:
      return (False, e)

    # self._handle.set_trace_callback(print)
    
    return (True, None)

  def close(self) -> bool:
    if self._handle:
      self._handle.close()
      return True

    return False

  def execute(self, sql: str, params: tuple[any] = ()) -> tuple[bool, str]:
    try:
      cursor = self._handle.cursor()
      cursor.execute(sql, params)
    except sqlite3.Error as e:
      return (False, str(e))
    
    return (True, None)

  def commit(self, sql: str, params: tuple[any]) -> bool:
    cursor = self._handle.cursor()
    
    last_row_id = cursor.lastrowid

    cursor.execute(sql, params)
    self._handle.commit()

    return last_row_id != cursor.lastrowid
    
  def query(self, 
            sql: str, 
            params: tuple[any] = (), 
            type: QueryType = QueryType.ALL,
            many_count: int = 1) -> tuple[any]:
    cursor = self._handle.cursor()
    cursor.execute(sql, params)

    if type == QueryType.ALL:
      rows = cursor.fetchall()
    elif type == QueryType.MANY:
      rows = cursor.fetchmany(many_count)
    elif type == QueryType.ONE:
      rows = cursor.fetchone()
    
    return rows
    