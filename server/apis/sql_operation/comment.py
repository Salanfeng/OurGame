from server.apis.sql_operation.macros import *

def comment_select(serial):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM comments WHERE serial = %d'
    cursor.execute(check_query, (serial))
    result = cursor.fetchone()
    closeSQL(conn, cursor)
    return result

def comment_insert(serial, userserial, gameserial, commentserial, content):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        users (serial, userserial, gameserial, commentserial, content)
        VALUE (%d, %d, %d, %d, %s);
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
            SET %s = %s + %d
            WHERE serial = %d
        '''
        cursor.execute(alter_query, (altertype, altertype, 1, serial))
    elif altertype == 'content':
        alter_query = '''
            UPDATE users
            SET content = %s
            WHERE serial = %d
        '''
        cursor.execute(alter_query, (content, serial))
    else:
        alter_query = '''
            UPDATE users
            SET %s = %d
            WHERE serial = %d
        '''
        cursor.execute(alter_query, (altertype, content, serial))
    closeSQL(conn, cursor)
    
def comment_select_DESC(agreeOrNot, limit):
    conn, cursor = connectSQL()
    select_query = '''
        SELECT * 
        FROM comments 
        WHERE COUNT(*) <= %d
        ORDERED BY %s DESC
    '''
    cursor.execute(select_query, (limit, agreeOrNot))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result