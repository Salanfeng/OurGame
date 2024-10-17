from macros import *

def useractivity_insert(activityserial, userserial):
    conn, cursor = connectSQL()
    insert_query = '''
        INSERT INTO 
        useractivity (activityserial, userserial, status)
        VALUE (%s, %s, %s);
    '''
    cursor.execute(insert_query, 
        (activityserial, userserial, 'ing'))
    closeSQL(conn, cursor)