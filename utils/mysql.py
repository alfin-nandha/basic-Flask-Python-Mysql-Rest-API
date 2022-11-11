import mysql.connector
import app

def db_conn():
    return mysql.connector.connect(
                host=app.app.config['DB_HOST'],
                database=app.app.config['DB_DATABASE'],
                user=app.app.config['DB_USERNAME'],
                password=app.app.config['DB_PASSWORD'])


def db_dconn(cur, conn):
    cur.close()
    conn.close()