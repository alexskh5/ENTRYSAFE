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
