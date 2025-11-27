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

    def update_home_pass(self, username, new_homepass):
        try:
            cur = self.conn.cursor()
            cur.execute("CALL update_home_pass(%s, %s);", (username, new_homepass))
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
