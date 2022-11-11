import bcrypt

from utils import mysql, response, token


def insert_user(data):
    conn = None
    cur = None
    sql = 'INSERT INTO users(name, email, password) VALUES (%s, %s, %s)'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()
        name = data['name']
        email = data['email']
        byte_password = data['password'].encode('utf-8')
        
        if name == None or email == None or byte_password== None:
            return response.fail_bad_request()

        salt = bcrypt.gensalt(rounds=16)
        hashed_password = bcrypt.hashpw(byte_password, salt).decode('utf-8')

        val = (name, email, hashed_password)
        cur.execute(sql, val)
        conn.commit()

        return response.success_create()

    except Exception as err:
        print("exception", err)
        if 'Duplicate' in err.msg:
            return response.email_already_exist()
        else:
            return response.internal_service_error()
    
    finally:
        mysql.db_dconn(cur, conn)

def get_all_users():
    conn = None
    cur = None
    sql = 'SELECT id, name, email FROM users'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()
        cur.execute(sql)
        rawDataList = cur.fetchall()

        data = [{
            'id':rawData[0],
            'name':rawData[1], 
            'email':rawData[2]} 
            for rawData in rawDataList]

        return response.success_get_data(data)

    except Exception as Err:
        print("Exception ", Err)
        return response.internal_service_error()

    finally:
        mysql.db_dconn(cur, conn)

def get_user_by_id(id):
    conn = None
    cur = None
    sql = 'SELECT id, name, email from users WHERE id = %s'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()
        cur.execute(sql, [id])
        rawData = cur.fetchone()
        
        if rawData == None:
            return response.fail_data_not_found()

        data = {
            'id':rawData[0],
            'name':rawData[1], 
            'email':rawData[2]}

        credentials = token.extract_token()
        if str(credentials['id']) != id:
            return response.fail_not_authorize()

        return response.success_get_data(data)

    except Exception as Err:
        print(Err)
        return response.internal_service_error()
        
    finally:
        mysql.db_dconn(cur, conn)

def delete_user_by_id(id):
    conn = None
    cur = None
    sql = 'delete from users where id = %s'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()
        cur.execute(sql, [id])
        
        if cur.rowcount == 0:
            return response.fail_data_not_found()

        conn.commit()

        return response.success_operation()

    except Exception as Err:
        print(Err)
        return response.internal_service_error()

    finally:
        mysql.db_dconn(cur, conn)
    

def update_user_by_id(data, id):
    conn = None
    cur = None
    sql = 'UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()
        
        rawResponse = get_user_by_id(id)

        if rawResponse[0].get_json()['code'] == 404:
            return response.fail_data_not_found()
        
        name = data['name']
        email = data['email']
        byte_password = data['password'].encode('utf-8')

        salt = bcrypt.gensalt(rounds=16)
        hashed_password = bcrypt.hashpw(byte_password, salt)

        val = (name, email, hashed_password, id)
        cur.execute(sql, val)
        conn.commit()

        return response.success_update()

    except Exception as Err:
        print(Err)
        return response.internal_service_error()
    
    finally:
        mysql.db_dconn(cur, conn)

def login(data):
    conn = None
    cur = None
    sql = 'SELECT id, name, email, password FROM users WHERE email=%s'

    try:
        conn = mysql.db_conn()
        cur = conn.cursor()

        email = data['email']
        byte_password = data['password'].encode('utf-8')

        if email == None or byte_password== None:
            return response.fail_bad_request()
        
        cur.execute(sql, [email])
        rawData = cur.fetchone()

        if rawData == None:
            return response.fail_login()
        
        data = {
            'id':rawData[0],
            'name':rawData[1],
            'email':rawData[2],
        }
        byte_hashed_password = rawData[3].encode('utf-8')
        
        isValid = bcrypt.checkpw(byte_password, byte_hashed_password)

        if isValid:
            data['token'] = token.generate_JWT(data['email'], data['id'])
            return response.success_login(data)
        else:
            return response.fail_login()
    
    except Exception as Err:
        print(Err)
        return response.internal_service_error()

    finally:
        mysql.db_dconn(cur, conn)
