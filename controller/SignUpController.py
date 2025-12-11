from database.connection import Database
import psycopg2

class SignupController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def signup(self, username, password, homepass, q1, a1, q2, a2):
        try:
            cur = self.conn.cursor()

            cur.execute("""
                CALL signup_user(%s, %s, %s, %s, %s, %s, %s)
            """, (username, password, homepass, q1, a1, q2, a2))

            self.conn.commit()
            return True, "Account created successfully!"

        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return False, "Username already exists."

        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def username_exists(self, username):
        """
        Returns True if username already exists (case-insensitive), else False.
        """
        cur = self.conn.cursor()
        cur.execute(
            "SELECT 1 FROM users WHERE LOWER(username) = LOWER(%s) LIMIT 1;",
            (username,)
        )
        row = cur.fetchone()
        return row is not None