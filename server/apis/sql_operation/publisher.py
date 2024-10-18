from server.apis.sql_operation.macros import *

def publisher_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM publishers WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def publisher_insert(serial, publishername, information):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        publishers(serial, publishername, information)
        VALUE (%s, %s, %s)
    '''
    cursor.execute(insert_query, 
                (serial, publishername, information))
    closeSQL(conn, cursor)