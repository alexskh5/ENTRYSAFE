# from datetime import datetime
# from database.connection import Database
# from psycopg2.extras import RealDictCursor   # ADD THIS


# class StudentController:
#     def __init__(self):
#         self.db = Database()
#         self.conn = self.db.connect()
#         self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)  # FIXED

#     # -------------------------------------------------
#     # Generate Student Code (S001, S002, ...)
#     # -------------------------------------------------
#     def generate_student_id(self, username):
#         self.cursor.execute("""
#             SELECT studID FROM students
#             WHERE username = %s
#             ORDER BY studID DESC LIMIT 1
#         """, (username,))

#         row = self.cursor.fetchone()

#         if row is None:
#             return "S001"

#         last_id = row["studID"]  # S005 ➝ 5 ➝ 6 ➝ S006
#         num = int(last_id[1:]) + 1
#         return f"S{num:03d}"

#     # -------------------------------------------------
#     # Load all students for this user
#     # -------------------------------------------------
#     def get_students(self, username):
#         self.cursor.execute("""
#             SELECT * FROM students
#             WHERE username = %s
#             ORDER BY createdAt ASC
#         """, (username,))
#         return self.cursor.fetchall()

#     # -------------------------------------------------
#     # Search
#     # -------------------------------------------------
#     def search_students(self, username, search):
#         like = f"%{search}%"
#         self.cursor.execute("""
#             SELECT * FROM students
#             WHERE username = %s AND (
#                 studID LIKE %s OR
#                 studFname LIKE %s OR
#                 studMname LIKE %s OR
#                 studLname LIKE %s
#             )
#             ORDER BY createdAt ASC
#         """, (username, like, like, like, like))
#         return self.cursor.fetchall()

#     # -------------------------------------------------
#     # Insert student
#     # -------------------------------------------------
#     def insert_student(self, username, data):
#         self.cursor.execute("""
#             INSERT INTO students(
#                 username,
#                 studID, studFname, studMname, studLname,
#                 studDOB, studSex,
#                 motherName, motherDOB,
#                 fatherName, fatherDOB,
#                 guardianName, guardianDOB,
#                 contact
#             )
#             VALUES (%(username)s, %(studID)s, %(studFname)s, %(studMname)s, %(studLname)s,
#                     %(studDOB)s, %(studSex)s,
#                     %(motherName)s, %(motherDOB)s,
#                     %(fatherName)s, %(fatherDOB)s,
#                     %(guardianName)s, %(guardianDOB)s,
#                     %(contact)s)
#         """, data)

#         self.conn.commit()
#         return True



from database.connection import Database
from psycopg2.extras import RealDictCursor


class StudentController:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    # -------------------------------------------------
    # Generate Student Code using DB FUNCTION
    # -------------------------------------------------
    def generate_student_id(self, username):
        self.cursor.execute("""
            SELECT next_student_code(%s) AS code;
        """, (username,))

        row = self.cursor.fetchone()
        return row["code"] if row else "S001"

    # -------------------------------------------------
    # Load all students for this user
    # -------------------------------------------------
    def get_students(self, username):
        self.cursor.execute("""
            SELECT *
            FROM students
            WHERE username = %s
            ORDER BY createdat ASC;
        """, (username,))
        return self.cursor.fetchall()

    # -------------------------------------------------
    # Search students
    # -------------------------------------------------
    def search_students(self, username, search):
        like = f"%{search}%"
        self.cursor.execute("""
            SELECT *
            FROM students
            WHERE username = %s
            AND (
                LOWER(studID) LIKE %s OR
                LOWER(studFname) LIKE %s OR
                LOWER(studMname) LIKE %s OR
                LOWER(studLname) LIKE %s
            )
            ORDER BY createdAt ASC
        """, (username, like, like, like, like))

        return self.cursor.fetchall()

    # -------------------------------------------------
    # Insert student (CALL PROCEDURE)
    # -------------------------------------------------
    def insert_student(self, username, data):
        self.cursor.execute("""
            CALL add_student(
                %(username)s,
                %(studID)s,
                %(studLname)s,
                %(studFname)s,
                %(studMname)s,
                %(studDOB)s,
                %(studSex)s,
                %(studContact)s,
                %(motherName)s,
                %(motherDOB)s,
                %(fatherName)s,
                %(fatherDOB)s,
                %(guardianName)s,
                %(guardianDOB)s
            );
        """, data)

        self.conn.commit()
        return True
