from server.apis.sql_operation.macros import *

def user_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM users WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchone()
    closeSQL(conn, cursor)
    return result

def user_insert(serial, username, nickname, password, role, email):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        users (serial, username, nickname, password, role, email, balance, avatar, introduction)
        VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    cursor.execute(insert_query, 
        (serial, username, nickname, password, role, email, '0.0', None, None))
    closeSQL(conn, cursor)
    
def user_update(serial, altertype, content):
    conn, cursor = connectSQL()
    alter_query = '''
        UPDATE users
        SET %s = %s
        WHERE serial = %s
    '''
    cursor.execute(alter_query, (altertype, content, serial))
    closeSQL(conn, cursor)
    
           