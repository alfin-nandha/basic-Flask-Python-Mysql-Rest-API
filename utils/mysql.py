import mysql.connector

def db_conn(app):
    return mysql.connector.connect(
                host=app.config['DB_HOST'],
                database=app.config['DB_DATABASE'],
                user=app.config['DB_USERNAME'],
                password=app.config['DB_PASSWORD'])


def db_dconn(cur, conn):
    cur.close()
    conn.close()