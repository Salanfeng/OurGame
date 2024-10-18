from server.apis.sql_operation.macros import *

def usercommunity_get(communityserial, userserial):
    conn, cursor = connectSQL()
    check_query = '''
        SELECT * FROM usercommunity 
        WHERE communityserial = %s
        AND userserial = %s
    '''
    cursor.execute(check_query, (communityserial, userserial))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def usercommunity_select(value, selectType='communityserial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM usercommunity WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def usercommunity_insert(communityserial, userserial):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        users (communityserial, userserial, role)
        VALUE (%s, %s, %s);
    '''
    cursor.execute(insert_query, 
        (communityserial, userserial, 'member'))
    closeSQL(conn, cursor)