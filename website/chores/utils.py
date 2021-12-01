""" Helper functions for the chore routes and package. """

from random import shuffle, seed
from sqlite3 import connect
from datetime import datetime as dt
from traceback import print_exc
from time import time

from website import db
from website.models import Tasks


def _db_connection(datab, query: str) -> list:
    """ Function to make sql connection to database.
    
    ARGS:
        datab: The database to connect to, pulled from calling function.
        query: The query to execute against the database.
    Return:
        List containing results.
    Raises:
        IOError / OSError: raises exception if cannot connect.
    """
    try:
        _conn = connect(datab)
        with _conn:
            _query_cursor = _conn.cursor()
            _query_cursor.execute(query)
            results = _query_cursor.fetchall()
            return results
    except (IOError, OSError):
        print_exc()


# TODO: Find a way to sort and split the chores using FLASK_SQLALCHEMY instead
def chore_sorting(database: str) -> None:
    """ This function gets the results of the SQL query and randomly assigns
    a user to a result item in the resulting list. Using a sql client 
    connection as the flask-sqlalchemy does not seem to return a an
    iterable.
    
    Args:
        database: The application database containing a table of
        household chores.
    """
    current_day = dt.today().weekday()
    if current_day < 5:
        sql_statement = "SELECT data FROM chore WHERE is_weekend IS FALSE;"
    else:
        sql_statement = "SELECT data FROM chore;"
    results = _db_connection(database, sql_statement)
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
