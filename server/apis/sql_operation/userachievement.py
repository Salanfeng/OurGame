from macros import *

def userachievement_select(userserial, gameserial, achievementserial):
    conn, cursor = connectSQL()
    check_query = '''
        SELECT * FROM userachievement 
        WHERE userserial = %s
        AND gameserial = %s
        AND achievementserial = %s
    '''
    cursor.execute(check_query, (userserial, gameserial, achievementserial))
    result = cursor.fetchall()
    closeSQL(conn, cursor)
    return result

def userachievement_insert(userserial, gameserial, achievementserial, time):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        userachievement (userserial, gameserial, achievementserial, time)
        VALUE (%s, %s, %s, %s);
    '''
    cursor.execute(insert_query, 
        (userserial, gameserial, achievementserial, time))
    closeSQL(conn, cursor)