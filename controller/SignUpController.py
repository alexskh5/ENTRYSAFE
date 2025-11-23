from database.connection import Database
import psycopg2

class SignupController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def signup(self, username, password, homepass):
        try:
            cur = self.conn.cursor()

            cur.execute("""
                CALL signup_user(%s, %s, %s)
            """, (username, password, homepass))

            self.conn.commit()
            return True, "Signup successful!"

        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return False, "Username already exists."

        except Exception as e:
            self.conn.rollback()
            return False, f"Error: {str(e)}"
