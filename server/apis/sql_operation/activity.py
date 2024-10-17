from server.apis.sql_operation.macros import *

def activity_select(value, selectType='serial'):
    conn, cursor = connectSQL()
    check_query = 'SELECT * FROM activities WHERE %s = %s'
    cursor.execute(check_query, (selectType, value))
    result = cursor.fetchone()
    closeSQL(conn, cursor)
    return result