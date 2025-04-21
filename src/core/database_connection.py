import psycopg2
import os

dbUser = os.environ["DB_USER"]
dbPassword = os.environ["DB_PASSWORD"]
dbName = os.environ["DB_NAME"]
DATABASE_URL = "postgres://" + dbUser + ":"+ dbPassword +"@bingle_db:5432/" + dbName

def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn