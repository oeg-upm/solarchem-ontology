import mysql.connector
from mysql.connector import errorcode
from conf.config import parser

config = {
  'user': parser.get("database", "user"),
  'password': parser.get("database", "password"),
  'host': parser.get("database", "host"),
  'database': parser.get("database", "database"),
  'raise_on_warnings': True
}

try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

  exit()
else:
  cursor = cnx.cursor(dictionary=True)
