from random import shuffle, seed
from sqlite3 import connect
from datetime import datetime as dt
from traceback import print_exc
from time import time
from website import db
from website.models import Tasks


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


def chore_sorting(datab):
    current_day = dt.today().weekday()
    if current_day < 5:
        sql_statement = "SELECT data FROM chore WHERE is_weekend IS FALSE;"
    else:
        sql_statement = "SELECT data FROM chore;"
    results = db_connection(str(datab), sql_statement)
    shuffle(results, seed(time()))
    chore_count = 0
    for iteration, row in enumerate(results):
        if chore_count < (int(len(results) / 2)):
            task = Tasks(task=row[0], user_id=3)
        else:
            task = Tasks(task=row[0], user_id=2)
        chore_count += 1
        db.session.add(task)
    db.session.commit()
    return None
