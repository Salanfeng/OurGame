from server.apis.sql_operation.macros import *

def comment_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM comments WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def comment_select_DESC(selectType, limit):
    conn, cursor = connectSQL()
    select_query = '''
        SELECT * 
        FROM comments 
        LIMIT %s
        ORDER BY %s DESC
    '''
    cursor.execute(select_query, (limit, selectType))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def comment_select_group_DESC(selectType, limit):
    conn, cursor = connectSQL()
    select_query = '''
        SELECT %s 
        FROM comments
        GROUP BY %s
        LIMIT %s
        ORDERED BY COUNT(*) DESC
    '''
    cursor.execute(select_query, (selectType, selectType, limit))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def comment_insert(serial, userserial, gameserial, commentserial, content):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        users (serial, userserial, gameserial, commentserial, content)
        VALUE (%s, %s, %s, %s, %s);
    '''
    cursor.execute(insert_query, 
        (serial, userserial, gameserial, commentserial, content))
    closeSQL(conn, cursor)
    
def comment_update(serial, altertype, content):
    conn, cursor = connectSQL()
    if altertype == 'agree'\
        or altertype == 'disagree':
        alter_query = '''
            UPDATE users
            SET %s = %s + %s
            WHERE serial = %s
        '''
        cursor.execute(alter_query, (altertype, altertype, '1', serial))
    else:
        alter_query = '''
            UPDATE users
            SET %s = %s
            WHERE serial = %s
        '''
        cursor.execute(alter_query, (altertype, content, serial))
    closeSQL(conn, cursor)

def comment_search(searchtype, keywords):
    conn, cursor = connectSQL()
    select_query = 'SELECT * FROM comments WHERE %s LIKE "%%s%"'
    cursor.execute(select_query, (searchtype, keywords))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result