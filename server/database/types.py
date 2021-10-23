from enum import IntEnum

class QueryType(IntEnum):
  ONE   = 1
  ALL   = 2
  MANY  = 3

class RequestType(IntEnum):
  EXECUTE = 0,
  COMMIT  = 1,
  QUERY   = 2

class ReturnCode(IntEnum):
  SUCCESS                   = 0,
  CONNECTION_FAILURE        = 1,
  PARAMETERS_COUNT_MISMATCH = 2,
  EXECUTE_FAILURE           = 3,
  COMMIT_FAILURE            = 4,
  SOMETHING_WENT_WRONG      = 5,
  UNKNOWN_COMMAND           = 6,
  UNKNOWN_OUTPUT            = 7,
  COMMUNICATION_FAILURE     = 8
