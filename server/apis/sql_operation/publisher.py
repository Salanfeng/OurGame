from server.apis.sql_operation.macros import *

def publisher_select(serial):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM publishers WHERE serial = %d'
    cursor.execute(check_query, (serial))
    result = cursor.fetchone()
    closeSQL(conn, cursor)
    return result

def publisher_insert(serial, publishername, information):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        publishers(serial, publishername, information)
        VALUE (%d, %s, %s)
    '''
    cursor.execute(insert_query, 
                (serial, publishername, information))
    closeSQL(conn, cursor)