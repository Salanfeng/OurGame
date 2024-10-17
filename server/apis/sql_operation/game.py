from server.apis.sql_operation.macros import *

def game_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    select_query = '''
        SELECT * 
        FROM games
        WHERE %s = %s
    '''
    cursor.execute(select_query, (selectType, value))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def game_insert(serial, gamename, gametype, publisher, information, price):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        games(serial, gamename, gametype, publisherSerial, information, price)
        VALUE (%s, %s, %s, %s, %s, %f)
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