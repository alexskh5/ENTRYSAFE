import psycopg2
from psycopg2.extras import RealDictCursor
from database.connection import Database

class AttendanceController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def search_attendance(self, username: str, term: str):
        self.cursor.execute(
            "SELECT * FROM get_attendance_records(%s, %s);",
            (username, term,)
        )

        return self.cursor.fetchall()
