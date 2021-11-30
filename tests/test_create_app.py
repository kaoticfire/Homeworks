from unittest import TestSuite
from tempfile import mkstemp
from website import create_app, create_database
from website.chores import chores_db_connection
from os import close, unlink


def test_create_app(TestCase):
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        temp_db = create_database()
        sql_statement = "SELECT data FROM chore;"
        chores_db_connection(temp_db).executescript(sql_statement)

    yield app

    # close and remove the temporary database
    close(db_fd)
    unlink(db_path)