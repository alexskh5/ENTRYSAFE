from database.connection import Database

class HomePassController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def validate_home_pass(self, username, homepass):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT verify_home_pass(%s, %s);", (username, homepass))
            result = cur.fetchone()[0]
            return bool(result)
        except Exception:
            return False

    def change_homepass_with_current(self, username, current_pass, new_pass):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "CALL change_user_homepass(%s, %s, %s)",
                (username, current_pass, new_pass)
            )
            self.conn.commit()
            return True, "Home pass updated."
        except Exception as e:
            self.conn.rollback()
            return False, str(e).splitlines()[0]

    def change_homepass_with_security(self, username, new_pass):
        try:
            cur = self.conn.cursor()
            cur.execute("CALL update_home_pass(%s, %s);", (username, new_pass))
            self.conn.commit()
            return True, "Home pass updated."
        except Exception as e:
            self.conn.rollback()
            return False, str(e).splitlines()[0]
