from random import shuffle
from sqlite3 import connect
from datetime import datetime as dt
from traceback import print_exc


def db_connection(db, query):
    try:
        _conn = connect(db)
        with _conn:
            _query_cursor = _conn.cursor()
            _query_cursor.execute(query)
            results = _query_cursor.fetchall()
            return results
    except (IOError, OSError):
        print_exc()


def chore_sorting(db):
    current_day = dt.today().weekday()
    if current_day < 5:
        sql_statement = "SELECT data FROM chore WHERE is_weekend = 1;"
    else:
        sql_statement = "SELECT data FROM chore;"
    results = db_connection(str(db), sql_statement)

    shuffle(results)
    chore_count = 0
    current_date = dt.today().strftime('%m-%d-%Y')
    m_bday = '02-14'
    j_bday = '02-20'
    m_chores = []
    j_chores = []

    for iteration, row in enumerate(results):
        if current_date.startswith(m_bday):
            j_chores.append(row[0])
        elif current_date.startswith(j_bday):
            m_chores.append(row[0])
        elif chore_count < (int(len(results) / 2)):
            m_chores.append(row[0])
        else:
            j_chores.append(row[0])
        chore_count += 1
    return m_chores, j_chores
