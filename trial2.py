import os
import mysql.connector

database = mysql.connector.connect(
  host = "localhost",
  user = os.environ.get("DB_USER"),
  password = os.environ.get("DB_PASS"),
  database = os.environ.get("DB_NAME")
)
cursor = database.cursor()


