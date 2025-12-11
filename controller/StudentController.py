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
    def search_students(self, username, term):
        try:
            sql = """
                SELECT 
                    studid,
                    studlname,
                    studfname,
                    studmname,
                    studcontact
                FROM students
                WHERE LOWER(username) = LOWER(%s)
                  AND (
                        LOWER(studlname) LIKE LOWER(%s)
                    OR  LOWER(studfname) LIKE LOWER(%s)
                    OR  LOWER(studmname) LIKE LOWER(%s)
                    OR  LOWER(studid) LIKE LOWER(%s)
                  )
                ORDER BY studlname ASC, studfname ASC;
            """

            like_term = f"%{term}%"
            self.cursor.execute(sql, (username, like_term, like_term, like_term, like_term))
            rows = self.cursor.fetchall()

            result = []
            for r in rows:
                result.append({
                    "studid": r["studid"],
                    "studlname": r["studlname"],
                    "studfname": r["studfname"],
                    "studmname": r["studmname"],
                    "studcontact": r["studcontact"],
                })

            return result

        except Exception as e:
            print("Error in search_students:", e)
            return []

    # -------------------------------------------------
    # Insert student (CALL PROCEDURE)
    # data must contain 'username' etc.
    # -------------------------------------------------
    def insert_student(self, data):
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

    # -------------------------------------------------
    # Get single student by username + studID (code)
    # -------------------------------------------------
    def get_student(self, username, studID):
        self.cursor.execute("""
            SELECT *
            FROM students
            WHERE username = %s
              AND studid = %s
            LIMIT 1;
        """, (username, studID))
        return self.cursor.fetchone()

    # -------------------------------------------------
    # Update student (CALL PROCEDURE)
    # data must contain 'username' and 'studID'
    # -------------------------------------------------
    def update_student(self, data):
        self.cursor.execute("""
            CALL update_student(
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

    # -------------------------------------------------
    # Delete student (per user)
    # -------------------------------------------------
    def delete_student(self, username, studID):
        self.cursor.execute("""
            CALL delete_student(%s, %s);
        """, (username, studID))
        self.conn.commit()
        return True
