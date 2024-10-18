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
    
def useractivity_update(activityserial, userserial, altertype, content):
    conn, cursor = connectSQL()
    alter_query = '''
        UPDATE useractivity
        SET %s = %s
        WHERE activityserial = %s
        AND userserial = %s
    '''
    cursor.execute(alter_query, (altertype, content, activityserial, userserial))
    closeSQL(conn, cursor)
    