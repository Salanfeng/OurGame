from server.apis.sql_operation.macros import *

def game_select(serial):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM games WHERE serial = %d'
    cursor.execute(check_query, (serial))
    result = cursor.fetchone()
    closeSQL(conn, cursor)
    return result

def game_insert(serial, gamename, gametype, publisher, information, price):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        games(serial, gamename, gametype, publisherSerial, information, price)
        VALUE (%d, %s, %s, %d, %s, %f)
    '''
    cursor.execute(insert_query, 
        (serial, gamename, gametype, publisher, information, price))
    closeSQL(conn, cursor)
    
def game_search(searchtype, keywords):
    conn, cursor = connectSQL()
    select_query = 'SELECT * FROM games WHERE %s LIKE "%%s%"'
    cursor.execute(select_query, (searchtype, keywords))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result