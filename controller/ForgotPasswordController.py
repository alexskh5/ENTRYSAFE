# from database.connection import Database

# class ForgotPasswordController:
#     def __init__(self):
#         self.db = Database()
#         self.conn = self.db.connect()

#     def get_questions(self):
#         try:
#             cur = self.conn.cursor()
#             cur.execute("SELECT * FROM get_security_questions()")
#             result = cur.fetchone()
#             return result  # (q1, q2)
#         except Exception:
#             return None

#     def verify_answers(self, a1, a2):
#         try:
#             cur = self.conn.cursor()
#             cur.execute("SELECT verify_security_answers(%s, %s)", (a1.lower(), a2.lower()))
#             result = cur.fetchone()
#             return bool(result[0])
#         except Exception:
#             return False

#     def update_password(self, new_pass):
#         try:
#             cur = self.conn.cursor()
#             cur.execute("CALL update_user_password(%s)", (new_pass,))
#             self.conn.commit()
#             return True
#         except Exception:
#             self.conn.rollback()
#             return False




from database.connection import Database
import psycopg2

class ForgotPasswordController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def get_questions(self, username):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT q1, q2 FROM get_security_questions(%s);", (username,))
            row = cur.fetchone()
            if not row:
                return False, "Username not found."
            return True, {"q1": row[0], "q2": row[1]}
        except Exception as e:
            return False, str(e)

    def verify_answers(self, username, a1, a2):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT verify_security_answers(%s, %s, %s);
            """, (username, a1, a2))
            result = cur.fetchone()[0]
            return (True, "Correct answers.") if result else (False, "Incorrect answers.")
        except Exception as e:
            return False, str(e)

    def update_password(self, username, new_pass):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CALL update_user_password(%s, %s);
            """, (username, new_pass))
            self.conn.commit()
            return True, "Password updated successfully."
        except Exception as e:
            self.conn.rollback()
            return False, str(e)