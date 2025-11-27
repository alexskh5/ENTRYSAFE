import os
import base64
import numpy as np
from database.connection import Database
from psycopg2.extras import RealDictCursor

UPLOAD_DIR = "uploads/guardians"

class GuardianController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    # -------------------------
    # Helper: encode face vector
    # -------------------------
    def encode_face(self, embedding):
        """Convert numpy array → base64 bytea for DB."""
        arr = np.array(embedding, dtype=np.float32)
        return base64.b64encode(arr.tobytes())

    def decode_face(self, bytea_data):
        if bytea_data is None:
            return None
        decoded = base64.b64decode(bytea_data)
        return np.frombuffer(decoded, dtype=np.float32)

    # -------------------------
    # Insert guardian
    # -------------------------
    def insert_guardian(self, studid, name, dob, image_path, encoding):
        self.cursor.execute("""
            CALL add_guardian(%s, %s, %s, %s, %s);
        """, (studid, name, dob, image_path, encoding))

        self.conn.commit()
        return True

    # -------------------------
    # Update guardian
    # -------------------------
    def update_guardian(self, guardianid, name, dob, image_path, encoding):
        self.cursor.execute("""
            CALL update_guardian(%s, %s, %s, %s, %s);
        """, (guardianid, name, dob, image_path, encoding))

        self.conn.commit()
        return True

    # -------------------------
    # Delete guardian
    # -------------------------
    def delete_guardian(self, guardianid):
        self.cursor.execute("CALL delete_guardian(%s)", (guardianid,))
        self.conn.commit()
        return True

    # -------------------------
    # Get guardians for a student
    # -------------------------
    def get_guardians_for_student(self, studid):
        self.cursor.execute("""
            SELECT * FROM get_guardians_for_student(%s);
        """, (studid,))
        return self.cursor.fetchall()
