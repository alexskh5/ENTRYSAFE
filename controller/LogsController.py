import psycopg2
from psycopg2.extras import RealDictCursor
from database.connection import Database

class LogsController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def search_logs(self, username, term):
        self.cursor.execute(
            "SELECT * FROM get_logs_records(%s, %s);",
            (username, term,)
        )
        return self.cursor.fetchall()
