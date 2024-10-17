from server.apis.sql_operation.macros import *

def usergame_insert(userserial, gameserial):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        usergame(userserial, gameserial)
        VALUE (%s, %s)
    '''
    cursor.execute(insert_query, (userserial, gameserial))
    closeSQL(conn, cursor)