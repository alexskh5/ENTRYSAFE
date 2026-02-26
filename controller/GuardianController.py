# import os
# import numpy as np
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from database.connection import Database
# from utils.paths import app_dir

# UPLOAD_DIR = os.path.join(app_dir(), "uploads", "guardians")


# class GuardianController:
#     def __init__(self):
#         self.db = Database()
#         self.conn = self.db.connect()
#         self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

#         self.verification_status = {}

        
#         self.verification_status = {}
        
        
#         # if not os.path.exists(UPLOAD_DIR):
#         #     os.makedirs(UPLOAD_DIR)
#         os.makedirs(UPLOAD_DIR, exist_ok=True)
        
#     def to_db_path(self, abs_path):
#         base = app_dir()
#         rel = os.path.relpath(abs_path, base)
#         return rel.replace("\\", "/")

#     def to_abs_path(self, db_path):
#         return os.path.join(app_dir(), db_path)

#     # ===============================================
#     # Encode / Decode face embedding
#     # ===============================================
#     def encode_face(self, embedding):
#         arr = np.array(embedding, dtype=np.float32)
#         return psycopg2.Binary(arr.tobytes())

#     def decode_face(self, bytea_data):
#         if bytea_data is None:
#             return None
#         return np.frombuffer(bytea_data, dtype=np.float32)

#     # ===============================================
#     # INSERT Guardian  (NOW: studentid INT, not studid code)
#     # ===============================================
#     def insert_guardian(self, studentid, name, dob, image_path, encoding):
#         print("🔥 INSERT GUARDIAN — Encoding type:", type(encoding))
#         self.cursor.execute("""
#             CALL add_guardian(%s, %s, %s, %s, %s::bytea);
#         """, (studentid, name, dob, image_path, encoding))
#         self.conn.commit()
#         return True

#     # ===============================================
#     # UPDATE Guardian
#     # ===============================================
#     def update_guardian(self, guardianid, name, dob, image_path, encoding):
#         self.cursor.execute("""
#             CALL update_guardian(%s, %s, %s, %s, %s::bytea);
#         """, (guardianid, name, dob, image_path, encoding))
#         self.conn.commit()
#         return True

#     # ===============================================
#     # DELETE Guardian
#     # ===============================================
#     def delete_guardian(self, guardianid):
#         self.cursor.execute("CALL delete_guardian(%s);", (guardianid,))
#         self.conn.commit()
#         return True

#     # ===============================================
#     # GET Guardians for student (by studentid INT)
#     # ===============================================
#     def get_guardians_for_student(self, studentid):
#         self.cursor.execute("""
#             SELECT * FROM get_guardians_for_student(%s);
#         """, (studentid,))
#         return self.cursor.fetchall()

#     # ===============================================
#     # Attendance / Logs by STUDENTID
#     # ===============================================
#     def call_dropoff(self, studentid, guardian_name, is_manual):
#         self.cursor.execute(
#             "CALL mark_dropoff(%s, %s, %s)",
#             (studentid, guardian_name, is_manual)
#         )
#         self.conn.commit()

#     def call_pickup(self, studentid, guardian_name, is_manual):
#         self.cursor.execute(
#             "CALL mark_pickup(%s, %s, %s)",
#             (studentid, guardian_name, is_manual)
#         )
#         self.conn.commit()

#     def get_today_attendance(self, studentid: int):
#         self.cursor.execute(
#             """
#             SELECT date, dropoff_time, pickup_time
#             FROM attendance
#             WHERE studentid = %s AND date = CURRENT_DATE
#             LIMIT 1;
#             """,
#             (studentid,)
#         )
#         return self.cursor.fetchone()

#     def update_dropoff_guardian(self, studentid, name):
#         sql = """
#             UPDATE logs
#             SET dropoff_by = %s
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """
#         self.cursor.execute(sql, (name, studentid))
#         self.conn.commit()

#     def update_pickup_guardian(self, studentid, name):
#         sql = """
#             UPDATE logs
#             SET pickup_by = %s
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """
#         self.cursor.execute(sql, (name, studentid))
#         self.conn.commit()

#     def get_guardian_by_id(self, guardianid):
#         self.cursor.execute("""
#             SELECT guardianid, studentid, guardianname, guardiandob,
#                    face_image_path, face_encoding
#             FROM guardians
#             WHERE guardianid = %s
#             LIMIT 1;
#         """, (guardianid,))
#         return self.cursor.fetchone()

#     def manual_dropoff(self, studentid, guardian_name):
#         # update attendance time
#         self.cursor.execute("""
#             UPDATE attendance
#             SET dropoff_time = NOW()
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """, (studentid,))

#         # update logs guardian name
#         self.cursor.execute("""
#             UPDATE logs
#             SET dropoff_by = %s
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """, (guardian_name, studentid))

#         self.conn.commit()

    
#     def manual_pickup(self, studentid, guardian_name):
#         # update attendance time
#         self.cursor.execute("""
#             UPDATE attendance
#             SET pickup_time = NOW()
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """, (studentid,))

#         # update logs guardian name
#         self.cursor.execute("""
#             UPDATE logs
#             SET pickup_by = %s
#             WHERE studentid = %s AND date = CURRENT_DATE;
#         """, (guardian_name, studentid))

#         self.conn.commit()
        
        
        
#     # mark waiting
#     def set_waiting_verification(self, studentid):
#         self.verification_status[studentid] = "WAITING"

#     # check waiting
#     def is_waiting_verification(self, studentid):
#         return self.verification_status.get(studentid) == "WAITING"

#     # clear temporary verification
#     def clear_verification(self, studentid):
#         self.verification_status.pop(studentid, None)




import os
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor

from database.connection import Database
from utils.paths import uploads_guardians_dir, uploads_root_dir


class GuardianController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        self.verification_status = {}

        # ✅ Ensure uploads dir exists in a WRITABLE location (not inside .app)
        # self.UPLOAD_DIR = os.path.join(writable_data_dir(), "uploads", "guardians")
        # os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        self.UPLOAD_DIR = uploads_guardians_dir()

    # ==============================
    # Path helpers (DB <-> filesystem)
    # ==============================
    def to_db_path(self, abs_path: str) -> str:
        """
        Store relative to uploads_root_dir() so DB values look like:
          uploads/guardians/xxx.jpg
        """
        base = uploads_root_dir()
        rel = os.path.relpath(abs_path, base)
        rel = rel.replace("\\", "/")
        # ensure it always starts with "uploads/..."
        if not rel.startswith("uploads/"):
            rel = "uploads/" + rel.lstrip("/")
        return rel

    def to_abs_path(self, db_path: str) -> str:
        """
        Convert DB path (uploads/guardians/xxx.jpg) to absolute path.
        """
        if not db_path:
            return None

        base = uploads_root_dir()

        # normalize db_path
        p = db_path.replace("\\", "/")
        if p.startswith("uploads/"):
            p = p[len("uploads/"):]  # -> guardians/xxx.jpg

        return os.path.join(base, p)
    # def to_db_path(self, abs_path: str) -> str:
    #     """
    #     Convert absolute path to a DB-storable relative path.
    #     Stored relative to writable_data_dir().

    #     Example stored in DB:
    #       uploads/guardians/S001_name_123.jpg
    #     """
    #     base = writable_data_dir()
    #     rel = os.path.relpath(abs_path, base)
    #     return rel.replace("\\", "/")

    # def to_abs_path(self, db_path: str) -> str:
    #     """
    #     Convert DB relative path back to absolute path in writable_data_dir().
    #     """
    #     if not db_path:
    #         return None
    #     base = writable_data_dir()
    #     return os.path.join(base, db_path)

    # ==============================
    # Encode / Decode face embedding
    # ==============================
    def encode_face(self, embedding):
        arr = np.array(embedding, dtype=np.float32)
        return psycopg2.Binary(arr.tobytes())

    def decode_face(self, bytea_data):
        if bytea_data is None:
            return None
        return np.frombuffer(bytea_data, dtype=np.float32)

    # ==============================
    # INSERT Guardian
    # studentid is INT
    # ==============================
    def insert_guardian(self, studentid, name, dob, image_path, encoding):
        self.cursor.execute(
            """
            CALL add_guardian(%s, %s, %s, %s, %s::bytea);
            """,
            (studentid, name, dob, image_path, encoding),
        )
        self.conn.commit()
        return True

    # ==============================
    # UPDATE Guardian
    # ==============================
    def update_guardian(self, guardianid, name, dob, image_path, encoding):
        self.cursor.execute(
            """
            CALL update_guardian(%s, %s, %s, %s, %s::bytea);
            """,
            (guardianid, name, dob, image_path, encoding),
        )
        self.conn.commit()
        return True

    # ==============================
    # DELETE Guardian
    # ==============================
    def delete_guardian(self, guardianid):
        self.cursor.execute("CALL delete_guardian(%s);", (guardianid,))
        self.conn.commit()
        return True

    # ==============================
    # GET Guardians for student
    # ==============================
    def get_guardians_for_student(self, studentid):
        self.cursor.execute("SELECT * FROM get_guardians_for_student(%s);", (studentid,))
        return self.cursor.fetchall()

    # ==============================
    # Attendance / Logs by STUDENTID
    # ==============================
    def call_dropoff(self, studentid, guardian_name, is_manual):
        self.cursor.execute("CALL mark_dropoff(%s, %s, %s)", (studentid, guardian_name, is_manual))
        self.conn.commit()

    def call_pickup(self, studentid, guardian_name, is_manual):
        self.cursor.execute("CALL mark_pickup(%s, %s, %s)", (studentid, guardian_name, is_manual))
        self.conn.commit()

    def get_today_attendance(self, studentid: int):
        self.cursor.execute(
            """
            SELECT date, dropoff_time, pickup_time
            FROM attendance
            WHERE studentid = %s AND date = CURRENT_DATE
            LIMIT 1;
            """,
            (studentid,),
        )
        return self.cursor.fetchone()

    def update_dropoff_guardian(self, studentid, name):
        self.cursor.execute(
            """
            UPDATE logs
            SET dropoff_by = %s
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (name, studentid),
        )
        self.conn.commit()

    def update_pickup_guardian(self, studentid, name):
        self.cursor.execute(
            """
            UPDATE logs
            SET pickup_by = %s
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (name, studentid),
        )
        self.conn.commit()

    def get_guardian_by_id(self, guardianid):
        self.cursor.execute(
            """
            SELECT guardianid, studentid, guardianname, guardiandob,
                   face_image_path, face_encoding
            FROM guardians
            WHERE guardianid = %s
            LIMIT 1;
            """,
            (guardianid,),
        )
        return self.cursor.fetchone()

    def manual_dropoff(self, studentid, guardian_name):
        self.cursor.execute(
            """
            UPDATE attendance
            SET dropoff_time = NOW()
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (studentid,),
        )
        self.cursor.execute(
            """
            UPDATE logs
            SET dropoff_by = %s
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (guardian_name, studentid),
        )
        self.conn.commit()

    def manual_pickup(self, studentid, guardian_name):
        self.cursor.execute(
            """
            UPDATE attendance
            SET pickup_time = NOW()
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (studentid,),
        )
        self.cursor.execute(
            """
            UPDATE logs
            SET pickup_by = %s
            WHERE studentid = %s AND date = CURRENT_DATE;
            """,
            (guardian_name, studentid),
        )
        self.conn.commit()

    # ==============================
    # Temporary verification flags
    # ==============================
    def set_waiting_verification(self, studentid):
        self.verification_status[studentid] = "WAITING"

    def is_waiting_verification(self, studentid):
        return self.verification_status.get(studentid) == "WAITING"

    def clear_verification(self, studentid):
        self.verification_status.pop(studentid, None)