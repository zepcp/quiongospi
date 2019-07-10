import logging

LOGGER = logging.getLogger("quiongos.db")

def execute(conn, sql, values=None, fetch=None, commit=False):
    sql = sql.strip()
    cursor = conn.cursor()
    LOGGER.debug(sql)
    LOGGER.debug(values)
    try:
        cursor.execute(sql, values)
    except Exception as exception:
        conn.commit()
        raise exception
    result = None
    if fetch == "all":
        result = cursor.fetchall()
    elif fetch == "one":
        result = cursor.fetchone()
    elif commit:
        conn.commit()
    cursor.close()
    return result

def exists(conn, table, criteria, values=None):
    sql = "select exists(select 1 from %s where %s)" % (table, criteria)
    return execute(conn, sql, values, fetch="one")[0]

def count(conn, table, criteria, values=None, counter=1):
    sql = "select count(%s) from %s where %s" % (counter, table, criteria)
    return execute(conn, sql, values, fetch="one")[0]
