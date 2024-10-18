from macros import *

def achievement_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM achievements WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def achievement_get(gameserial, achievementserial):
    conn, cursor = connectSQL()
    check_query = '''
        SELECT * FROM achievements
        WHERE gameserial = %s
        AND serial = %s
    '''
    cursor.execute(check_query, (gameserial, achievementserial))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result