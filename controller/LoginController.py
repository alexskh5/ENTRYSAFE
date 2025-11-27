from database.connection import Database

class LoginController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def login(self, username, password):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM login_user(%s, %s)", (username, password))
            result = cur.fetchone()

            if result:
                return True, result  # (userid, username)
            return False, "Invalid username or password."

        except Exception as e:
            return False, str(e)
