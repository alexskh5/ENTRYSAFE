-- -- DROP TABLE IF EXISTS users CASCADE;


-- -- CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- -- CREATE TABLE users (
-- --     userid SERIAL PRIMARY KEY,

-- --     username VARCHAR(255) NOT NULL UNIQUE,
-- --     userpassword TEXT NOT NULL,
-- --     userhomepass TEXT,

-- --     q1 TEXT NOT NULL,
-- --     a1 TEXT NOT NULL,
-- --     q2 TEXT NOT NULL,
-- --     a2 TEXT NOT NULL,

-- --     createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- -- );



-- -- CREATE OR REPLACE PROCEDURE signup_user(
-- --     p_username VARCHAR,
-- --     p_password VARCHAR,
-- --     p_homepass VARCHAR,
-- --     p_q1 TEXT,
-- --     p_a1 TEXT,
-- --     p_q2 TEXT,
-- --     p_a2 TEXT
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     INSERT INTO users (
-- --         username, userpassword, userhomepass,
-- --         q1, a1, q2, a2
-- --     )
-- --     VALUES (
-- --         p_username,
-- --         crypt(p_password, gen_salt('bf')),
-- --         CASE WHEN p_homepass IS NULL OR p_homepass = ''
-- --              THEN NULL
-- --              ELSE crypt(p_homepass, gen_salt('bf'))
-- --         END,
-- --         p_q1,
-- --         crypt(lower(p_a1), gen_salt('bf')),
-- --         p_q2,
-- --         crypt(lower(p_a2), gen_salt('bf'))
-- --     );
-- -- END;
-- -- $$;




-- -- CREATE OR REPLACE FUNCTION login_user(
-- --     p_username VARCHAR,
-- --     p_password VARCHAR
-- -- )
-- -- RETURNS TABLE(
-- --     userid INT,
-- --     username VARCHAR
-- -- )
-- -- AS $$
-- -- BEGIN
-- --     RETURN QUERY
-- --     SELECT u.userid, u.username
-- --     FROM users u
-- --     WHERE LOWER(u.username) = LOWER(p_username)
-- --       AND u.userpassword = crypt(p_password, u.userpassword);
-- -- END;
-- -- $$ LANGUAGE plpgsql;



-- -- CREATE OR REPLACE FUNCTION get_security_questions(p_username TEXT)
-- -- RETURNS TABLE(q1 TEXT, q2 TEXT)
-- -- AS $$
-- -- BEGIN
-- --     RETURN QUERY
-- --     SELECT u.q1, u.q2
-- --     FROM users u
-- --     WHERE LOWER(username) = LOWER(p_username);
-- -- END;
-- -- $$ LANGUAGE plpgsql;




-- -- CREATE OR REPLACE FUNCTION verify_security_answers(
-- --     p_username TEXT,
-- --     p_a1 TEXT,
-- --     p_a2 TEXT
-- -- )
-- -- RETURNS BOOLEAN
-- -- AS $$
-- -- BEGIN
-- --     RETURN EXISTS (
-- --         SELECT 1 FROM users
-- --         WHERE LOWER(username) = LOWER(p_username)
-- --           AND a1 = crypt(lower(p_a1), a1)
-- --           AND a2 = crypt(lower(p_a2), a2)
-- --     );
-- -- END;
-- -- $$ LANGUAGE plpgsql;




-- -- CREATE OR REPLACE PROCEDURE update_user_password(
-- --     p_username TEXT,
-- --     p_new_password TEXT
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     UPDATE users
-- --     SET userpassword = crypt(p_new_password, gen_salt('bf'))
-- --     WHERE LOWER(username) = LOWER(p_username);
-- -- END;
-- -- $$;




-- -- DELETE FROM users
-- -- WHERE username = 'admin';


-- -- SELECT * FROM users;



-- -- CREATE OR REPLACE FUNCTION verify_home_pass(
-- --     p_username TEXT,
-- --     p_homepass TEXT
-- -- )
-- -- RETURNS BOOLEAN
-- -- AS $$
-- -- BEGIN
-- --     RETURN EXISTS (
-- --         SELECT 1
-- --         FROM users
-- --         WHERE LOWER(username) = LOWER(p_username)
-- --           AND userhomepass = crypt(p_homepass, userhomepass)
-- --     );
-- -- END;
-- -- $$ LANGUAGE plpgsql;


-- -- CREATE OR REPLACE PROCEDURE update_home_pass(
-- --     p_username TEXT,
-- --     p_new_homepass TEXT
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     UPDATE users
-- --     SET userhomepass = crypt(p_new_homepass, gen_salt('bf'))
-- --     WHERE LOWER(username) = LOWER(p_username);
-- -- END;
-- -- $$;









-- -- DROP TABLE IF EXISTS students CASCADE;

-- -- CREATE TABLE students (
-- --     studentid SERIAL PRIMARY KEY,

-- --     -- FK to users table
-- --     username VARCHAR(255) NOT NULL,
-- --     CONSTRAINT fk_student_user
-- --         FOREIGN KEY (username)
-- --         REFERENCES users(username)
-- --         ON UPDATE CASCADE
-- --         ON DELETE CASCADE,

-- --     studID VARCHAR(20) NOT NULL UNIQUE,  -- S001, S002, etc.

-- --     studLname VARCHAR(255) NOT NULL,
-- --     studFname VARCHAR(255) NOT NULL,
-- --     studMname VARCHAR(255),

-- --     studDOB DATE,
-- --     studSex VARCHAR(20) NOT NULL,

-- --     studContact VARCHAR(50) NOT NULL,

-- --     motherName VARCHAR(255) NOT NULL,
-- --     motherDOB DATE,

-- --     fatherName VARCHAR(255),
-- --     fatherDOB DATE,

-- --     guardianName VARCHAR(255),
-- --     guardianDOB DATE,

-- --     createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- -- );



-- -- CREATE OR REPLACE FUNCTION next_student_code(p_username VARCHAR)
-- -- RETURNS VARCHAR
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     last_code VARCHAR;
-- --     last_num  INT;
-- -- BEGIN
-- --     SELECT studID
-- --     INTO last_code
-- --     FROM students
-- --     WHERE username = p_username
-- --     ORDER BY studentid DESC
-- --     LIMIT 1;

-- --     IF last_code IS NULL THEN
-- --         RETURN 'S001';
-- --     END IF;

-- --     -- get numeric part, assume format 'Snnn'
-- --     last_num := COALESCE(NULLIF(SUBSTRING(last_code FROM 2), ''), '0')::INT;
-- --     last_num := last_num + 1;

-- --     RETURN 'S' || LPAD(last_num::TEXT, 3, '0');
-- -- END;
-- -- $$;





-- -- CREATE OR REPLACE PROCEDURE add_student(
-- --     p_username      VARCHAR,
-- --     p_studID        VARCHAR,
-- --     p_studLname     VARCHAR,
-- --     p_studFname     VARCHAR,
-- --     p_studMname     VARCHAR,
-- --     p_studDOB       DATE,
-- --     p_studSex       VARCHAR,
-- --     p_studContact   VARCHAR,
-- --     p_motherName    VARCHAR,
-- --     p_motherDOB     DATE,
-- --     p_fatherName    VARCHAR,
-- --     p_fatherDOB     DATE,
-- --     p_guardianName  VARCHAR,
-- --     p_guardianDOB   DATE
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     INSERT INTO students (
-- --         username,
-- --         studID,
-- --         studLname, studFname, studMname,
-- --         studDOB, studSex,
-- --         studContact,
-- --         motherName, motherDOB,
-- --         fatherName, fatherDOB,
-- --         guardianName, guardianDOB
-- --     ) VALUES (
-- --         p_username,
-- --         p_studID,
-- --         p_studLname, p_studFname, p_studMname,
-- --         p_studDOB, p_studSex,
-- --         p_studContact,
-- --         p_motherName, p_motherDOB,
-- --         p_fatherName, p_fatherDOB,
-- --         p_guardianName, p_guardianDOB
-- --     );
-- -- END;
-- -- $$;



-- -- select * from students;


-- -- CREATE OR REPLACE PROCEDURE update_student(
-- --     p_studID        VARCHAR,
-- --     p_studLname     VARCHAR,
-- --     p_studFname     VARCHAR,
-- --     p_studMname     VARCHAR,
-- --     p_studDOB       DATE,
-- --     p_studSex       VARCHAR,
-- --     p_studContact   VARCHAR,
-- --     p_motherName    VARCHAR,
-- --     p_motherDOB     DATE,
-- --     p_fatherName    VARCHAR,
-- --     p_fatherDOB     DATE,
-- --     p_guardianName  VARCHAR,
-- --     p_guardianDOB   DATE
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     UPDATE students
-- --     SET
-- --         studLname = p_studLname,
-- --         studFname = p_studFname,
-- --         studMname = p_studMname,
-- --         studDOB = p_studDOB,
-- --         studSex = p_studSex,
-- --         studContact = p_studContact,
-- --         motherName = p_motherName,
-- --         motherDOB = p_motherDOB,
-- --         fatherName = p_fatherName,
-- --         fatherDOB = p_fatherDOB,
-- --         guardianName = p_guardianName,
-- --         guardianDOB = p_guardianDOB
-- --     WHERE studID = p_studID;
-- -- END;
-- -- $$;











-- -- DROP TABLE IF EXISTS guardians CASCADE;

-- -- CREATE TABLE guardians (
-- --     guardianid SERIAL PRIMARY KEY,

-- --     studid VARCHAR(20) NOT NULL,
-- --     FOREIGN KEY (studid)
-- --         REFERENCES students(studID)
-- --         ON UPDATE CASCADE
-- --         ON DELETE CASCADE,

-- --     guardianname VARCHAR(255) NOT NULL,
-- --     guardiandob DATE,
    
-- --     face_image_path TEXT,
-- --     face_encoding BYTEA,

-- --     createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- -- );




-- -- CREATE OR REPLACE PROCEDURE add_guardian(
-- --     p_studid VARCHAR,
-- --     p_name VARCHAR,
-- --     p_dob DATE,
-- --     p_image_path TEXT,
-- --     p_encoding BYTEA
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     INSERT INTO guardians (
-- --         studid, guardianname, guardiandob,
-- --         face_image_path, face_encoding
-- --     )
-- --     VALUES (
-- --         p_studid, p_name, p_dob,
-- --         p_image_path, p_encoding
-- --     );
-- -- END;
-- -- $$;



-- -- DROP PROCEDURE update_guardian(integer,character varying,date,text,bytea)


-- -- CREATE OR REPLACE PROCEDURE update_guardian(
-- --     p_guardianid INT,
-- --     p_name VARCHAR,
-- --     p_dob DATE,
-- --     p_image_path TEXT,
-- --     p_encoding BYTEA
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     UPDATE guardians
-- --     SET guardianname = p_name,
-- --         guardiandob = p_dob,
-- --         face_image_path = p_image_path,
-- --         face_encoding = p_encoding
-- --     WHERE guardianid = p_guardianid;
-- -- END;
-- -- $$;






-- -- CREATE OR REPLACE PROCEDURE delete_guardian(p_guardianid INT)
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     DELETE FROM guardians WHERE guardianid = p_guardianid;
-- -- END;
-- -- $$;



-- -- DROP FUNCTION IF EXISTS get_guardians_for_student(VARCHAR);

-- -- DROP FUNCTION get_guardians_for_student(character varying)

-- -- CREATE OR REPLACE FUNCTION get_guardians_for_student(p_studid VARCHAR)
-- -- RETURNS TABLE(
-- --     guardianid INT,
-- --     guardianname VARCHAR,
-- --     guardiandob DATE,
-- --     face_image_path TEXT,
-- --     face_encoding BYTEA,        -- 🔥 ADD THIS
-- --     studid VARCHAR
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     RETURN QUERY
-- --     SELECT 
-- --         g.guardianid,
-- --         g.guardianname,
-- --         g.guardiandob,
-- --         g.face_image_path,
-- --         g.face_encoding,        -- 🔥 ADD THIS
-- --         g.studid
-- --     FROM guardians g
-- --     WHERE g.studid = p_studid
-- --     ORDER BY g.guardianid ASC;
-- -- END;
-- -- $$;







-- -- CREATE TABLE attendance (
-- --     attendanceid SERIAL PRIMARY KEY,
    
-- --     studid VARCHAR(20) NOT NULL REFERENCES students(studID)
-- --         ON UPDATE CASCADE ON DELETE CASCADE,

-- --     date DATE NOT NULL,
-- --     dropoff_time TIMESTAMP,
-- --     pickup_time TIMESTAMP,

-- --     CONSTRAINT unique_student_date UNIQUE (studid, date)
-- -- );






-- -- CREATE TABLE logs (
-- --     logid SERIAL PRIMARY KEY,

-- --     studid VARCHAR(20) NOT NULL REFERENCES students(studID)
-- --         ON UPDATE CASCADE ON DELETE CASCADE,

-- --     date DATE NOT NULL,
-- --     studentname VARCHAR(255) NOT NULL,

-- --     dropoff_by VARCHAR(255),
-- --     pickup_by VARCHAR(255)
-- -- );





-- -- CREATE OR REPLACE PROCEDURE mark_dropoff(
-- --     p_studid VARCHAR,
-- --     p_guardian_name VARCHAR,
-- --     p_manual BOOLEAN
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     today DATE := CURRENT_DATE;
-- -- BEGIN
-- --     -- Create attendance row if missing
-- --     INSERT INTO attendance (studid, date, dropoff_time)
-- --     VALUES (p_studid, today, NOW())
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET dropoff_time = EXCLUDED.dropoff_time;

-- --     -- Insert OR update logs
-- --     INSERT INTO logs (studid, date, studentname, dropoff_by)
-- --     VALUES (
-- --         p_studid,
-- --         today,
-- --         (SELECT studlname || ', ' || studfname FROM students WHERE studID = p_studid),
-- --         CASE WHEN p_manual THEN 'MANUAL (' || p_guardian_name || ')' ELSE p_guardian_name END
-- --     )
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET dropoff_by = EXCLUDED.dropoff_by;
-- -- END;
-- -- $$;






-- -- CREATE OR REPLACE PROCEDURE mark_pickup(
-- --     p_studid VARCHAR,
-- --     p_guardian_name VARCHAR,
-- --     p_manual BOOLEAN
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     today DATE := CURRENT_DATE;
-- -- BEGIN
-- --     UPDATE attendance
-- --     SET pickup_time = NOW()
-- --     WHERE studid = p_studid AND date = today;

-- --     INSERT INTO logs (studid, date, studentname, pickup_by)
-- --     VALUES (
-- --         p_studid,
-- --         today,
-- --         (SELECT studlname || ', ' || studfname FROM students WHERE studID = p_studid),
-- --         CASE WHEN p_manual THEN 'MANUAL (' || p_guardian_name || ')' ELSE p_guardian_name END
-- --     )
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET pickup_by = EXCLUDED.pickup_by;
-- -- END;
-- -- $$;



-- -- SELECT username, studid, studlname FROM students;


-- -- select * from students;

-- -- SELECT guardianid, guardianname, face_encoding
-- -- FROM guardians;

-- -- SELECT guardianid, guardianname, face_encoding
-- -- FROM guardians;


-- -- DELETE FROM guardians WHERE studid = 'S001';


-- -- SELECT guardianid, guardianname, octet_length(face_encoding) AS size
-- -- FROM guardians;



-- -- DELETE FROM logs a
-- -- USING logs b
-- -- WHERE
-- --     a.logid < b.logid
-- --     AND a.studid = b.studid
-- --     AND a.date = b.date;


-- -- ALTER TABLE logs
-- -- ADD CONSTRAINT unique_log_per_day UNIQUE (studid, date);

-- -- ON CONFLICT (studid, date)

-- -- select * from logs;

-- -- select * from attendance;

-- -- delete from logs where logid = 17;

-- -- delete from attendance where attendanceid = 14;


-- -- DROP PROCEDURE mark_dropoff(character varying,character varying,boolean);
-- -- CREATE OR REPLACE PROCEDURE mark_dropoff(
-- --     p_studid        VARCHAR,
-- --     p_guardian_name VARCHAR,
-- --     p_verified      BOOLEAN
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     today DATE := CURRENT_DATE;
-- --     v_studentname VARCHAR(255);
-- -- BEGIN
-- --     SELECT studlname || ', ' || studfname
-- --     INTO v_studentname
-- --     FROM students
-- --     WHERE studID = p_studid;

-- --     -- Ensure attendance row exists, set dropoff_time
-- --     INSERT INTO attendance (studid, date, dropoff_time)
-- --     VALUES (p_studid, today, NOW())
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET dropoff_time = EXCLUDED.dropoff_time;

-- --     -- Insert or update logs for drop-off
-- --     INSERT INTO logs (studid, date, studentname, dropoff_by)
-- --     VALUES (
-- --         p_studid,
-- --         today,
-- --         v_studentname,
-- --         CASE 
-- --             WHEN p_verified THEN p_guardian_name
-- --             ELSE 'UNVERIFIED GUARDIAN'
-- --         END
-- --     )
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET dropoff_by = EXCLUDED.dropoff_by;
-- -- END;
-- -- $$;



-- -- DROP PROCEDURE mark_pickup(character varying,character varying,boolean);

-- -- CREATE OR REPLACE PROCEDURE mark_pickup(
-- --     p_studid        VARCHAR,
-- --     p_guardian_name VARCHAR,
-- --     p_verified      BOOLEAN
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     today DATE := CURRENT_DATE;
-- --     v_studentname VARCHAR(255);
-- -- BEGIN
-- --     SELECT studlname || ', ' || studfname
-- --     INTO v_studentname
-- --     FROM students
-- --     WHERE studID = p_studid;

-- --     -- Ensure attendance row exists, set pickup_time
-- --     INSERT INTO attendance (studid, date, pickup_time)
-- --     VALUES (p_studid, today, NOW())
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET pickup_time = EXCLUDED.pickup_time;

-- --     -- Insert or update logs for pick-up
-- --     INSERT INTO logs (studid, date, studentname, pickup_by)
-- --     VALUES (
-- --         p_studid,
-- --         today,
-- --         v_studentname,
-- --         CASE 
-- --             WHEN p_verified THEN p_guardian_name
-- --             ELSE 'UNVERIFIED GUARDIAN'
-- --         END
-- --     )
-- --     ON CONFLICT (studid, date)
-- --     DO UPDATE SET pickup_by = EXCLUDED.pickup_by;
-- -- END;
-- -- $$;



-- -- -- Change password
-- -- CREATE OR REPLACE PROCEDURE change_user_password(
-- --     p_username TEXT,
-- --     p_current_password TEXT,
-- --     p_new_password TEXT
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     v_userid INT;
-- -- BEGIN
-- --     SELECT userid
-- --     INTO v_userid
-- --     FROM users
-- --     WHERE LOWER(username) = LOWER(p_username)
-- --       AND userpassword = crypt(p_current_password, userpassword);

-- --     IF v_userid IS NULL THEN
-- --         RAISE EXCEPTION 'Current password is incorrect.';
-- --     END IF;

-- --     IF LENGTH(p_new_password) < 8
-- --        OR p_new_password !~ '[A-Z]'
-- --        OR p_new_password !~ '[a-z]'
-- --        OR p_new_password !~ '[0-9]' THEN
-- --         RAISE EXCEPTION 'Password must be at least 8 characters long, include uppercase, lowercase, and a number.';
-- --     END IF;

-- --     UPDATE users
-- --     SET userpassword = crypt(p_new_password, gen_salt('bf'))
-- --     WHERE userid = v_userid;

-- -- END;
-- -- $$;


-- -- --Change home pass
-- -- CREATE OR REPLACE PROCEDURE change_user_homepass(
-- --     p_username TEXT,
-- --     p_current_homepass TEXT,
-- --     p_new_homepass TEXT
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- DECLARE
-- --     v_userid INT;
-- -- BEGIN
-- --     SELECT userid
-- --     INTO v_userid
-- --     FROM users
-- --     WHERE LOWER(username) = LOWER(p_username)
-- --       AND userhomepass = crypt(p_current_homepass, userhomepass);

-- --     IF v_userid IS NULL THEN
-- --         RAISE EXCEPTION 'Current home password is incorrect.';
-- --     END IF;

-- --     UPDATE users
-- --     SET userhomepass = crypt(p_new_homepass, gen_salt('bf'))
-- --     WHERE userid = v_userid;
-- -- END;
-- -- $$;



-- -- --Update username
-- -- CREATE OR REPLACE PROCEDURE update_username(
-- --     p_old_username VARCHAR,
-- --     p_new_username VARCHAR>>>>>>> 077e2484a002f5375a50aafd03a57e0f50308d61

-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- -- <<<<<<< HEAD
-- --     IF EXISTS (SELECT 1 FROM users WHERE LOWER(username) = LOWER(p_new_username)) THEN
-- --         RAISE EXCEPTION 'Username "%" already exists.', p_new_username;
-- --     END IF;

-- --     UPDATE users
-- --     SET username = p_new_username
-- --     WHERE LOWER(username) = LOWER(p_old_username);

-- --     -- Because of ON UPDATE CASCADE, students.username is updated automatically
-- -- END;
-- -- $$;



-- -- CREATE OR REPLACE PROCEDURE delete_student(p_studid VARCHAR)
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     DELETE FROM students WHERE studID = p_studid;
-- -- END;
-- -- $$;



-- -- CREATE OR REPLACE FUNCTION get_attendance_records(
-- --     p_username VARCHAR,
-- --     p_search TEXT
-- -- )
-- -- RETURNS TABLE(
-- --     date DATE,
-- --     studid VARCHAR,
-- --     studentname VARCHAR,
-- --     dropoff_by VARCHAR,
-- --     pickup_by VARCHAR,
-- --     dropoff_time TIMESTAMP,
-- --     pickup_time TIMESTAMP
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     RETURN QUERY
-- --     SELECT 
-- --         a.date,
-- --         a.studid,
-- --         (SELECT (studlname || ', ' || studfname)::VARCHAR FROM students s WHERE s.studID = a.studid),
-- --         l.dropoff_by,
-- --         l.pickup_by,
-- --         a.dropoff_time,
-- --         a.pickup_time
-- --     FROM attendance a
-- --     JOIN logs l ON l.studid = a.studid AND l.date = a.date
-- --     JOIN students s ON s.studID = a.studid
-- --     WHERE s.username = p_username
-- --       AND (
-- --             p_search IS NULL OR p_search = '' OR
-- --             a.studid ILIKE '%' || p_search || '%' OR
-- --             (s.studlname || ' ' || s.studfname) ILIKE '%' || p_search || '%' OR
-- --             a.date::TEXT ILIKE '%' || p_search || '%'
-- --       )
-- --     ORDER BY a.date DESC;
-- -- END;
-- -- $$;



-- -- CREATE OR REPLACE FUNCTION get_logs_records(
-- --     p_username VARCHAR,
-- --     p_search TEXT
-- -- )
-- -- RETURNS TABLE(
-- --     date_display TEXT,
-- --     studentname VARCHAR,
-- --     dropoff_by VARCHAR,
-- --     pickup_by VARCHAR
-- -- )
-- -- LANGUAGE plpgsql
-- -- AS $$
-- -- BEGIN
-- --     RETURN QUERY
-- --     SELECT
-- --         to_char(a.dropoff_time, 'YYYY-MM-DD HH24:MI:SS'), -- real time!!
-- --         l.studentname,
-- --         l.dropoff_by,
-- --         l.pickup_by
-- --     FROM logs l
-- --     JOIN students s ON s.studID = l.studid
-- --     LEFT JOIN attendance a
-- --         ON a.studid = l.studid AND a.date = l.date
-- --     WHERE s.username = p_username
-- --       AND (
-- --             p_search IS NULL OR p_search = '' OR
-- --             l.studentname ILIKE '%' || p_search || '%' OR
-- --             l.dropoff_by ILIKE '%' || p_search || '%' OR
-- --             l.pickup_by ILIKE '%' || p_search || '%' OR
-- --             l.date::TEXT ILIKE '%' || p_search || '%'
-- --       )
-- --     ORDER BY l.date DESC;
-- -- END;
-- -- $$;


-- -- CREATE OR REPLACE FUNCTION is_same_password(
-- --     p_username TEXT,
-- --     p_new_password TEXT
-- -- )
-- -- RETURNS BOOLEAN
-- -- AS $$
-- -- BEGIN
-- --     RETURN EXISTS (
-- --         SELECT 1
-- --         FROM users
-- --         WHERE LOWER(username) = LOWER(p_username)
-- --           AND userpassword = crypt(p_new_password, userpassword)
-- --     );
-- -- END;
-- -- $$ LANGUAGE plpgsql;



-- -- ===========================================
-- -- EXTENSIONS
-- -- ===========================================
-- CREATE EXTENSION IF NOT EXISTS PGCRYPTO;


-- -- ===========================================
-- -- USERS TABLE + FUNCTIONS/PROCEDURES
-- -- ===========================================
-- DROP TABLE IF EXISTS USERS CASCADE;

-- CREATE TABLE USERS (
--     USERID SERIAL PRIMARY KEY,
--     USERNAME VARCHAR(255) NOT NULL UNIQUE,
--     USERPASSWORD TEXT NOT NULL,
--     USERHOMEPASS TEXT,
--     Q1 TEXT NOT NULL,
--     A1 TEXT NOT NULL,
--     Q2 TEXT NOT NULL,
--     A2 TEXT NOT NULL,
--     CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE OR REPLACE PROCEDURE SIGNUP_USER(
--     P_USERNAME VARCHAR,
--     P_PASSWORD VARCHAR,
--     P_HOMEPASS VARCHAR,
--     P_Q1 TEXT,
--     P_A1 TEXT,
--     P_Q2 TEXT,
--     P_A2 TEXT
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     INSERT INTO USERS (
--         USERNAME, USERPASSWORD, USERHOMEPASS,
--         Q1, A1, Q2, A2
--     )
--     VALUES (
--         P_USERNAME,
--         CRYPT(P_PASSWORD, GEN_SALT('BF')),
--         CASE WHEN P_HOMEPASS IS NULL OR P_HOMEPASS = ''
--              THEN NULL
--              ELSE CRYPT(P_HOMEPASS, GEN_SALT('BF'))
--         END,
--         P_Q1,
--         CRYPT(LOWER(P_A1), GEN_SALT('BF')),
--         P_Q2,
--         CRYPT(LOWER(P_A2), GEN_SALT('BF'))
--     );
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION LOGIN_USER(
--     P_USERNAME VARCHAR,
--     P_PASSWORD VARCHAR
-- )
-- RETURNS TABLE(
--     USERID INT,
--     USERNAME VARCHAR
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT U.USERID, U.USERNAME
--     FROM USERS U
--     WHERE LOWER(U.USERNAME) = LOWER(P_USERNAME)
--       AND U.USERPASSWORD = CRYPT(P_PASSWORD, U.USERPASSWORD);
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION GET_SECURITY_QUESTIONS(P_USERNAME TEXT)
-- RETURNS TABLE(Q1 TEXT, Q2 TEXT)
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT U.Q1, U.Q2
--     FROM USERS U
--     WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION VERIFY_SECURITY_ANSWERS(
--     P_USERNAME TEXT,
--     P_A1 TEXT,
--     P_A2 TEXT
-- )
-- RETURNS BOOLEAN
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN EXISTS (
--         SELECT 1 FROM USERS
--         WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
--           AND A1 = CRYPT(LOWER(P_A1), A1)
--           AND A2 = CRYPT(LOWER(P_A2), A2)
--     );
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE UPDATE_USER_PASSWORD(
--     P_USERNAME TEXT,
--     P_NEW_PASSWORD TEXT
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     UPDATE USERS
--     SET USERPASSWORD = CRYPT(P_NEW_PASSWORD, GEN_SALT('BF'))
--     WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION VERIFY_HOME_PASS(
--     P_USERNAME TEXT,
--     P_HOMEPASS TEXT
-- )
-- RETURNS BOOLEAN
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN EXISTS (
--         SELECT 1
--         FROM USERS
--         WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
--           AND USERHOMEPASS = CRYPT(P_HOMEPASS, USERHOMEPASS)
--     );
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE UPDATE_HOME_PASS(
--     P_USERNAME TEXT,
--     P_NEW_HOMEPASS TEXT
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     UPDATE USERS
--     SET USERHOMEPASS = CRYPT(P_NEW_HOMEPASS, GEN_SALT('BF'))
--     WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE CHANGE_USER_PASSWORD(
--     P_USERNAME TEXT,
--     P_CURRENT_PASSWORD TEXT,
--     P_NEW_PASSWORD TEXT
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- DECLARE
--     V_USERID INT;
-- BEGIN
--     SELECT USERID
--     INTO V_USERID
--     FROM USERS
--     WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
--       AND USERPASSWORD = CRYPT(P_CURRENT_PASSWORD, USERPASSWORD);

--     IF V_USERID IS NULL THEN
--         RAISE EXCEPTION 'CURRENT PASSWORD IS INCORRECT.';
--     END IF;

--     IF LENGTH(P_NEW_PASSWORD) < 8
--        OR P_NEW_PASSWORD !~ '[A-Z]'
--        OR P_NEW_PASSWORD !~ '[a-z]'
--        OR P_NEW_PASSWORD !~ '[0-9]' THEN
--         RAISE EXCEPTION 'PASSWORD MUST BE AT LEAST 8 CHARACTERS WITH UPPERCASE, LOWERCASE, AND NUMBER.';
--     END IF;

--     UPDATE USERS
--     SET USERPASSWORD = CRYPT(P_NEW_PASSWORD, GEN_SALT('BF'))
--     WHERE USERID = V_USERID;
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE CHANGE_USER_HOMEPASS(
--     P_USERNAME TEXT,
--     P_CURRENT_HOMEPASS TEXT,
--     P_NEW_HOMEPASS TEXT
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- DECLARE
--     V_USERID INT;
-- BEGIN
--     SELECT USERID
--     INTO V_USERID
--     FROM USERS
--     WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
--       AND USERHOMEPASS = CRYPT(P_CURRENT_HOMEPASS, USERHOMEPASS);

--     IF V_USERID IS NULL THEN
--         RAISE EXCEPTION 'CURRENT HOME PASS IS INCORRECT.';
--     END IF;

--     UPDATE USERS
--     SET USERHOMEPASS = CRYPT(P_NEW_HOMEPASS, GEN_SALT('BF'))
--     WHERE USERID = V_USERID;
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE UPDATE_USERNAME(
--     P_OLD_USERNAME VARCHAR,
--     P_NEW_USERNAME VARCHAR
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     IF EXISTS (SELECT 1 FROM USERS WHERE LOWER(USERNAME) = LOWER(P_NEW_USERNAME)) THEN
--         RAISE EXCEPTION 'USERNAME "%" ALREADY EXISTS.', P_NEW_USERNAME;
--     END IF;

--     UPDATE USERS
--     SET USERNAME = P_NEW_USERNAME
--     WHERE LOWER(USERNAME) = LOWER(P_OLD_USERNAME);
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION IS_SAME_PASSWORD(
--     P_USERNAME TEXT,
--     P_NEW_PASSWORD TEXT
-- )
-- RETURNS BOOLEAN
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN EXISTS (
--         SELECT 1
--         FROM USERS
--         WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
--           AND USERPASSWORD = CRYPT(P_NEW_PASSWORD, USERPASSWORD)
--     );
-- END;
-- $$;


-- -- ===========================================
-- -- STUDENTS TABLE + FUNCTIONS/PROCEDURES
-- -- ===========================================
-- DROP TABLE IF EXISTS STUDENTS CASCADE;

-- CREATE TABLE STUDENTS (
--     STUDENTID SERIAL PRIMARY KEY,
--     USERNAME VARCHAR(255) NOT NULL,
--     CONSTRAINT FK_STUDENT_USER FOREIGN KEY (USERNAME)
--         REFERENCES USERS(USERNAME)
--         ON UPDATE CASCADE ON DELETE CASCADE,
--     STUDID VARCHAR(20) NOT NULL UNIQUE,
--     STUDLNAME VARCHAR(255) NOT NULL,
--     STUDFNAME VARCHAR(255) NOT NULL,
--     STUDMNAME VARCHAR(255),
--     STUDDOB DATE,
--     STUDSEX VARCHAR(20) NOT NULL,
--     STUDCONTACT VARCHAR(50) NOT NULL,
--     MOTHERNAME VARCHAR(255) NOT NULL,
--     MOTHERDOB DATE,
--     FATHERNAME VARCHAR(255),
--     FATHERDOB DATE,
--     GUARDIANNAME VARCHAR(255),
--     GUARDIANDOB DATE,
--     CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE OR REPLACE FUNCTION NEXT_STUDENT_CODE(P_USERNAME VARCHAR)
-- RETURNS VARCHAR
-- LANGUAGE PLPGSQL
-- AS $$
-- DECLARE
--     LAST_CODE VARCHAR;
--     LAST_NUM INT;
-- BEGIN
--     SELECT STUDID INTO LAST_CODE
--     FROM STUDENTS
--     WHERE USERNAME = P_USERNAME
--     ORDER BY STUDENTID DESC
--     LIMIT 1;

--     IF LAST_CODE IS NULL THEN
--         RETURN 'S001';
--     END IF;

--     LAST_NUM := COALESCE(NULLIF(SUBSTRING(LAST_CODE FROM 2), ''), '0')::INT + 1;

--     RETURN 'S' || LPAD(LAST_NUM::TEXT, 3, '0');
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE ADD_STUDENT(
--     P_USERNAME VARCHAR,
--     P_STUDID VARCHAR,
--     P_STUDLNAME VARCHAR,
--     P_STUDFNAME VARCHAR,
--     P_STUDMNAME VARCHAR,
--     P_STUDDOB DATE,
--     P_STUDSEX VARCHAR,
--     P_STUDCONTACT VARCHAR,
--     P_MOTHERNAME VARCHAR,
--     P_MOTHERDOB DATE,
--     P_FATHERNAME VARCHAR,
--     P_FATHERDOB DATE,
--     P_GUARDIANNAME VARCHAR,
--     P_GUARDIANDOB DATE
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     INSERT INTO STUDENTS (
--         USERNAME, STUDID, STUDLNAME, STUDFNAME, STUDMNAME,
--         STUDDOB, STUDSEX, STUDCONTACT,
--         MOTHERNAME, MOTHERDOB, FATHERNAME, FATHERDOB,
--         GUARDIANNAME, GUARDIANDOB
--     )
--     VALUES (
--         P_USERNAME, P_STUDID, P_STUDLNAME, P_STUDFNAME, P_STUDMNAME,
--         P_STUDDOB, P_STUDSEX, P_STUDCONTACT,
--         P_MOTHERNAME, P_MOTHERDOB, P_FATHERNAME, P_FATHERDOB,
--         P_GUARDIANNAME, P_GUARDIANDOB
--     );
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE UPDATE_STUDENT(
--     P_STUDID VARCHAR,
--     P_STUDLNAME VARCHAR,
--     P_STUDFNAME VARCHAR,
--     P_STUDMNAME VARCHAR,
--     P_STUDDOB DATE,
--     P_STUDSEX VARCHAR,
--     P_STUDCONTACT VARCHAR,
--     P_MOTHERNAME VARCHAR,
--     P_MOTHERDOB DATE,
--     P_FATHERNAME VARCHAR,
--     P_FATHERDOB DATE,
--     P_GUARDIANNAME VARCHAR,
--     P_GUARDIANDOB DATE
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     UPDATE STUDENTS
--     SET STUDLNAME = P_STUDLNAME,
--         STUDFNAME = P_STUDFNAME,
--         STUDMNAME = P_STUDMNAME,
--         STUDDOB = P_STUDDOB,
--         STUDSEX = P_STUDSEX,
--         STUDCONTACT = P_STUDCONTACT,
--         MOTHERNAME = P_MOTHERNAME,
--         MOTHERDOB = P_MOTHERDOB,
--         FATHERNAME = P_FATHERNAME,
--         FATHERDOB = P_FATHERDOB,
--         GUARDIANNAME = P_GUARDIANNAME,
--         GUARDIANDOB = P_GUARDIANDOB
--     WHERE STUDID = P_STUDID;
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE DELETE_STUDENT(P_STUDID VARCHAR)
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     DELETE FROM STUDENTS WHERE STUDID = P_STUDID;
-- END;
-- $$;


-- -- ===========================================
-- -- GUARDIANS TABLE + FUNCTIONS/PROCEDURES
-- -- ===========================================
-- DROP TABLE IF EXISTS GUARDIANS CASCADE;

-- CREATE TABLE GUARDIANS (
--     GUARDIANID SERIAL PRIMARY KEY,
--     STUDID VARCHAR(20) NOT NULL REFERENCES STUDENTS(STUDID)
--         ON UPDATE CASCADE ON DELETE CASCADE,
--     GUARDIANNAME VARCHAR(255) NOT NULL,
--     GUARDIANDOB DATE,
--     FACE_IMAGE_PATH TEXT,
--     FACE_ENCODING BYTEA,
--     CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE OR REPLACE PROCEDURE ADD_GUARDIAN(
--     P_STUDID VARCHAR,
--     P_NAME VARCHAR,
--     P_DOB DATE,
--     P_IMAGE_PATH TEXT,
--     P_ENCODING BYTEA
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     INSERT INTO GUARDIANS (
--         STUDID, GUARDIANNAME, GUARDIANDOB,
--         FACE_IMAGE_PATH, FACE_ENCODING
--     )
--     VALUES (
--         P_STUDID, P_NAME, P_DOB,
--         P_IMAGE_PATH, P_ENCODING
--     );
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE UPDATE_GUARDIAN(
--     P_GUARDIANID INT,
--     P_NAME VARCHAR,
--     P_DOB DATE,
--     P_IMAGE_PATH TEXT,
--     P_ENCODING BYTEA
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     UPDATE GUARDIANS
--     SET GUARDIANNAME = P_NAME,
--         GUARDIANDOB = P_DOB,
--         FACE_IMAGE_PATH = P_IMAGE_PATH,
--         FACE_ENCODING = P_ENCODING
--     WHERE GUARDIANID = P_GUARDIANID;
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE DELETE_GUARDIAN(P_GUARDIANID INT)
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     DELETE FROM GUARDIANS WHERE GUARDIANID = P_GUARDIANID;
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION GET_GUARDIANS_FOR_STUDENT(P_STUDID VARCHAR)
-- RETURNS TABLE(
--     GUARDIANID INT,
--     GUARDIANNAME VARCHAR,
--     GUARDIANDOB DATE,
--     FACE_IMAGE_PATH TEXT,
--     FACE_ENCODING BYTEA,
--     STUDID VARCHAR
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         G.GUARDIANID,
--         G.GUARDIANNAME,
--         G.GUARDIANDOB,
--         G.FACE_IMAGE_PATH,
--         G.FACE_ENCODING,
--         G.STUDID
--     FROM GUARDIANS G
--     WHERE G.STUDID = P_STUDID
--     ORDER BY G.GUARDIANID ASC;
-- END;
-- $$;


-- -- ===========================================
-- -- ATTENDANCE & LOGS TABLES + PROCEDURES
-- -- ===========================================
-- CREATE TABLE ATTENDANCE (
--     ATTENDANCEID SERIAL PRIMARY KEY,
--     STUDID VARCHAR(20) NOT NULL REFERENCES STUDENTS(STUDID)
--         ON UPDATE CASCADE ON DELETE CASCADE,
--     DATE DATE NOT NULL,
--     DROPOFF_TIME TIMESTAMP,
--     PICKUP_TIME TIMESTAMP,
--     CONSTRAINT UNIQUE_STUDENT_DATE UNIQUE (STUDID, DATE)
-- );

-- CREATE TABLE LOGS (
--     LOGID SERIAL PRIMARY KEY,
--     STUDID VARCHAR(20) NOT NULL REFERENCES STUDENTS(STUDID)
--         ON UPDATE CASCADE ON DELETE CASCADE,
--     DATE DATE NOT NULL,
--     STUDENTNAME VARCHAR(255) NOT NULL,
--     DROPOFF_BY VARCHAR(255),
--     PICKUP_BY VARCHAR(255),
--     CONSTRAINT UNIQUE_LOG_PER_DAY UNIQUE (STUDID, DATE)
-- );

-- CREATE OR REPLACE PROCEDURE MARK_DROPOFF(
--     P_STUDID VARCHAR,
--     P_GUARDIAN_NAME VARCHAR,
--     P_VERIFIED BOOLEAN
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- DECLARE
--     TODAY DATE := CURRENT_DATE;
--     V_STUDENTNAME VARCHAR(255);
-- BEGIN
--     SELECT STUDLNAME || ', ' || STUDFNAME
--     INTO V_STUDENTNAME
--     FROM STUDENTS
--     WHERE STUDID = P_STUDID;

--     INSERT INTO ATTENDANCE (STUDID, DATE, DROPOFF_TIME)
--     VALUES (P_STUDID, TODAY, NOW())
--     ON CONFLICT (STUDID, DATE)
--     DO UPDATE SET DROPOFF_TIME = EXCLUDED.DROPOFF_TIME;

--     INSERT INTO LOGS (STUDID, DATE, STUDENTNAME, DROPOFF_BY)
--     VALUES (
--         P_STUDID,
--         TODAY,
--         V_STUDENTNAME,
--         CASE WHEN P_VERIFIED THEN P_GUARDIAN_NAME ELSE 'UNVERIFIED GUARDIAN' END
--     )
--     ON CONFLICT (STUDID, DATE)
--     DO UPDATE SET DROPOFF_BY = EXCLUDED.DROPOFF_BY;
-- END;
-- $$;

-- CREATE OR REPLACE PROCEDURE MARK_PICKUP(
--     P_STUDID VARCHAR,
--     P_GUARDIAN_NAME VARCHAR,
--     P_VERIFIED BOOLEAN
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- DECLARE
--     TODAY DATE := CURRENT_DATE;
--     V_STUDENTNAME VARCHAR(255);
-- BEGIN
--     SELECT STUDLNAME || ', ' || STUDFNAME
--     INTO V_STUDENTNAME
--     FROM STUDENTS
--     WHERE STUDID = P_STUDID;

--     INSERT INTO ATTENDANCE (STUDID, DATE, PICKUP_TIME)
--     VALUES (P_STUDID, TODAY, NOW())
--     ON CONFLICT (STUDID, DATE)
--     DO UPDATE SET PICKUP_TIME = EXCLUDED.PICKUP_TIME;

--     INSERT INTO LOGS (STUDID, DATE, STUDENTNAME, PICKUP_BY)
--     VALUES (
--         P_STUDID,
--         TODAY,
--         V_STUDENTNAME,
--         CASE WHEN P_VERIFIED THEN P_GUARDIAN_NAME ELSE 'UNVERIFIED GUARDIAN' END
--     )
--     ON CONFLICT (STUDID, DATE)
--     DO UPDATE SET PICKUP_BY = EXCLUDED.PICKUP_BY;
-- END;
-- $$;


-- -- ===========================================
-- -- REPORT FUNCTIONS
-- -- ===========================================
-- CREATE OR REPLACE FUNCTION GET_ATTENDANCE_RECORDS(
--     P_USERNAME VARCHAR,
--     P_SEARCH TEXT
-- )
-- RETURNS TABLE(
--     DATE DATE,
--     STUDID VARCHAR,
--     STUDENTNAME VARCHAR,
--     DROPOFF_BY VARCHAR,
--     PICKUP_BY VARCHAR,
--     DROPOFF_TIME TIMESTAMP,
--     PICKUP_TIME TIMESTAMP
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
--         A.DATE,
--         A.STUDID,
--         (SELECT (STUDLNAME || ', ' || STUDFNAME)::VARCHAR FROM STUDENTS S WHERE S.STUDID = A.STUDID),
--         L.DROPOFF_BY,
--         L.PICKUP_BY,
--         A.DROPOFF_TIME,
--         A.PICKUP_TIME
--     FROM ATTENDANCE A
--     JOIN LOGS L ON L.STUDID = A.STUDID AND L.DATE = A.DATE
--     JOIN STUDENTS S ON S.STUDID = A.STUDID
--     WHERE S.USERNAME = P_USERNAME
--       AND (
--             P_SEARCH IS NULL OR P_SEARCH = '' OR
--             A.STUDID ILIKE '%' || P_SEARCH || '%' OR
--             (S.STUDLNAME || ' ' || S.STUDFNAME) ILIKE '%' || P_SEARCH || '%' OR
--             A.DATE::TEXT ILIKE '%' || P_SEARCH || '%'
--       )
--     ORDER BY A.DATE DESC;
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION GET_LOGS_RECORDS(
--     P_USERNAME VARCHAR,
--     P_SEARCH TEXT
-- )
-- RETURNS TABLE(
--     DATE_DISPLAY TEXT,
--     STUDENTNAME VARCHAR,
--     DROPOFF_BY VARCHAR,
--     PICKUP_BY VARCHAR
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         TO_CHAR(A.DROPOFF_TIME, 'YYYY-MM-DD HH24:MI:SS'),
--         L.STUDENTNAME,
--         L.DROPOFF_BY,
--         L.PICKUP_BY
--     FROM LOGS L
--     JOIN STUDENTS S ON S.STUDID = L.STUDID
--     LEFT JOIN ATTENDANCE A
--         ON A.STUDID = L.STUDID AND A.DATE = L.DATE
--     WHERE S.USERNAME = P_USERNAME
--       AND (
--             P_SEARCH IS NULL OR P_SEARCH = '' OR
--             L.STUDENTNAME ILIKE '%' || P_SEARCH || '%' OR
--             L.DROPOFF_BY ILIKE '%' || P_SEARCH || '%' OR
--             L.PICKUP_BY ILIKE '%' || P_SEARCH || '%' OR
--             L.DATE::TEXT ILIKE '%' || P_SEARCH || '%'
--       )
--     ORDER BY L.DATE DESC;
-- END;
-- $$;






-- ALTER TABLE guardians DROP CONSTRAINT guardians_studid_fkey;
-- ALTER TABLE attendance DROP CONSTRAINT attendance_studid_fkey;
-- ALTER TABLE logs DROP CONSTRAINT logs_studid_fkey;


-- ALTER TABLE students DROP CONSTRAINT students_studid_key;


-- ALTER TABLE students
-- ADD CONSTRAINT unique_stud_per_user UNIQUE (username, studid);


-- ALTER TABLE guardians ADD COLUMN studentid INT;
-- ALTER TABLE attendance ADD COLUMN studentid INT;
-- ALTER TABLE logs ADD COLUMN studentid INT;


-- UPDATE guardians g
-- SET studentid = s.studentid
-- FROM students s
-- WHERE g.studid = s.studid;

-- UPDATE attendance a
-- SET studentid = s.studentid
-- FROM students s
-- WHERE a.studid = s.studid;

-- UPDATE logs l
-- SET studentid = s.studentid
-- FROM students s
-- WHERE l.studid = s.studid;

-- ALTER TABLE guardians ALTER COLUMN studentid SET NOT NULL;
-- ALTER TABLE attendance ALTER COLUMN studentid SET NOT NULL;
-- ALTER TABLE logs ALTER COLUMN studentid SET NOT NULL;


-- ALTER TABLE guardians DROP CONSTRAINT IF EXISTS guardians_studid_fkey;
-- ALTER TABLE attendance DROP CONSTRAINT IF EXISTS attendance_studid_fkey;
-- ALTER TABLE logs DROP CONSTRAINT IF EXISTS logs_studid_fkey;


-- ALTER TABLE guardians DROP COLUMN studid;
-- ALTER TABLE attendance DROP COLUMN studid;
-- ALTER TABLE logs DROP COLUMN studid;


-- ALTER TABLE guardians
-- ADD CONSTRAINT guardians_studentid_fkey FOREIGN KEY (studentid)
-- REFERENCES students(studentid)
-- ON UPDATE CASCADE ON DELETE CASCADE;

-- ALTER TABLE attendance
-- ADD CONSTRAINT attendance_studentid_fkey FOREIGN KEY (studentid)
-- REFERENCES students(studentid)
-- ON UPDATE CASCADE ON DELETE CASCADE;

-- ALTER TABLE logs
-- ADD CONSTRAINT logs_studentid_fkey FOREIGN KEY (studentid)
-- REFERENCES students(studentid)
-- ON UPDATE CASCADE ON DELETE CASCADE;


-- CREATE OR REPLACE FUNCTION get_guardians_for_student(p_studentid INT)
-- RETURNS TABLE(
--     guardianid INT,
--     guardianname VARCHAR,
--     guardiandob DATE,
--     face_image_path TEXT,
--     face_encoding BYTEA,
--     studentid INT
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
--         g.guardianid,
--         g.guardianname,
--         g.guardiandob,
--         g.face_image_path,
--         g.face_encoding,
--         g.studentid
--     FROM guardians g
--     WHERE g.studentid = p_studentid
--     ORDER BY g.guardianid;
-- END;
-- $$;




CREATE EXTENSION IF NOT EXISTS PGCRYPTO;


-- ===========================================
-- USERS TABLE + FUNCTIONS/PROCEDURES
-- ===========================================
DROP TABLE IF EXISTS ATTENDANCE CASCADE;
DROP TABLE IF EXISTS LOGS CASCADE;
DROP TABLE IF EXISTS GUARDIANS CASCADE;
DROP TABLE IF EXISTS STUDENTS CASCADE;
DROP TABLE IF EXISTS USERS CASCADE;


CREATE TABLE USERS (
    USERID SERIAL PRIMARY KEY,
    USERNAME VARCHAR(255) NOT NULL UNIQUE,
    USERPASSWORD TEXT NOT NULL,
    USERHOMEPASS TEXT,
    Q1 TEXT NOT NULL,
    A1 TEXT NOT NULL,
    Q2 TEXT NOT NULL,
    A2 TEXT NOT NULL,
    CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE SIGNUP_USER(
    P_USERNAME VARCHAR,
    P_PASSWORD VARCHAR,
    P_HOMEPASS VARCHAR,
    P_Q1 TEXT,
    P_A1 TEXT,
    P_Q2 TEXT,
    P_A2 TEXT
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    INSERT INTO USERS (
        USERNAME, USERPASSWORD, USERHOMEPASS,
        Q1, A1, Q2, A2
    )
    VALUES (
        P_USERNAME,
        CRYPT(P_PASSWORD, GEN_SALT('BF')),
        CASE WHEN P_HOMEPASS IS NULL OR P_HOMEPASS = ''
             THEN NULL
             ELSE CRYPT(P_HOMEPASS, GEN_SALT('BF'))
        END,
        P_Q1,
        CRYPT(LOWER(P_A1), GEN_SALT('BF')),
        P_Q2,
        CRYPT(LOWER(P_A2), GEN_SALT('BF'))
    );
END;
$$;

CREATE OR REPLACE FUNCTION LOGIN_USER(
    P_USERNAME VARCHAR,
    P_PASSWORD VARCHAR
)
RETURNS TABLE(
    USERID INT,
    USERNAME VARCHAR
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN QUERY
    SELECT U.USERID, U.USERNAME
    FROM USERS U
    WHERE LOWER(U.USERNAME) = LOWER(P_USERNAME)
      AND U.USERPASSWORD = CRYPT(P_PASSWORD, U.USERPASSWORD);
END;
$$;

CREATE OR REPLACE FUNCTION GET_SECURITY_QUESTIONS(P_USERNAME TEXT)
RETURNS TABLE(Q1 TEXT, Q2 TEXT)
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN QUERY
    SELECT U.Q1, U.Q2
    FROM USERS U
    WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
END;
$$;

CREATE OR REPLACE FUNCTION VERIFY_SECURITY_ANSWERS(
    P_USERNAME TEXT,
    P_A1 TEXT,
    P_A2 TEXT
)
RETURNS BOOLEAN
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM USERS
        WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
          AND A1 = CRYPT(LOWER(P_A1), A1)
          AND A2 = CRYPT(LOWER(P_A2), A2)
    );
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_USER_PASSWORD(
    P_USERNAME TEXT,
    P_NEW_PASSWORD TEXT
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    UPDATE USERS
    SET USERPASSWORD = CRYPT(P_NEW_PASSWORD, GEN_SALT('BF'))
    WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
END;
$$;

CREATE OR REPLACE FUNCTION VERIFY_HOME_PASS(
    P_USERNAME TEXT,
    P_HOMEPASS TEXT
)
RETURNS BOOLEAN
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM USERS
        WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
          AND USERHOMEPASS = CRYPT(P_HOMEPASS, USERHOMEPASS)
    );
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_HOME_PASS(
    P_USERNAME TEXT,
    P_NEW_HOMEPASS TEXT
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    UPDATE USERS
    SET USERHOMEPASS = CRYPT(P_NEW_HOMEPASS, GEN_SALT('BF'))
    WHERE LOWER(USERNAME) = LOWER(P_USERNAME);
END;
$$;

CREATE OR REPLACE PROCEDURE CHANGE_USER_PASSWORD(
    P_USERNAME TEXT,
    P_CURRENT_PASSWORD TEXT,
    P_NEW_PASSWORD TEXT
)
LANGUAGE PLPGSQL
AS $$
DECLARE
    V_USERID INT;
BEGIN
    SELECT USERID
    INTO V_USERID
    FROM USERS
    WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
      AND USERPASSWORD = CRYPT(P_CURRENT_PASSWORD, USERPASSWORD);

    IF V_USERID IS NULL THEN
        RAISE EXCEPTION 'CURRENT PASSWORD IS INCORRECT.';
    END IF;

    IF LENGTH(P_NEW_PASSWORD) < 8
       OR P_NEW_PASSWORD !~ '[A-Z]'
       OR P_NEW_PASSWORD !~ '[a-z]'
       OR P_NEW_PASSWORD !~ '[0-9]' THEN
        RAISE EXCEPTION 'PASSWORD MUST BE AT LEAST 8 CHARACTERS WITH UPPERCASE, LOWERCASE, AND NUMBER.';
    END IF;

    UPDATE USERS
    SET USERPASSWORD = CRYPT(P_NEW_PASSWORD, GEN_SALT('BF'))
    WHERE USERID = V_USERID;
END;
$$;

CREATE OR REPLACE PROCEDURE CHANGE_USER_HOMEPASS(
    P_USERNAME TEXT,
    P_CURRENT_HOMEPASS TEXT,
    P_NEW_HOMEPASS TEXT
)
LANGUAGE PLPGSQL
AS $$
DECLARE
    V_USERID INT;
BEGIN
    SELECT USERID
    INTO V_USERID
    FROM USERS
    WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
      AND USERHOMEPASS = CRYPT(P_CURRENT_HOMEPASS, USERHOMEPASS);

    IF V_USERID IS NULL THEN
        RAISE EXCEPTION 'CURRENT HOME PASS IS INCORRECT.';
    END IF;

    UPDATE USERS
    SET USERHOMEPASS = CRYPT(P_NEW_HOMEPASS, GEN_SALT('BF'))
    WHERE USERID = V_USERID;
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_USERNAME(
    P_OLD_USERNAME VARCHAR,
    P_NEW_USERNAME VARCHAR
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM USERS WHERE LOWER(USERNAME) = LOWER(P_NEW_USERNAME)) THEN
        RAISE EXCEPTION 'USERNAME "%" ALREADY EXISTS.', P_NEW_USERNAME;
    END IF;

    UPDATE USERS
    SET USERNAME = P_NEW_USERNAME
    WHERE LOWER(USERNAME) = LOWER(P_OLD_USERNAME);
END;
$$;

CREATE OR REPLACE FUNCTION IS_SAME_PASSWORD(
    P_USERNAME TEXT,
    P_NEW_PASSWORD TEXT
)
RETURNS BOOLEAN
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM USERS
        WHERE LOWER(USERNAME) = LOWER(P_USERNAME)
          AND USERPASSWORD = CRYPT(P_NEW_PASSWORD, USERPASSWORD)
    );
END;
$$;


-- ===========================================
-- STUDENTS TABLE + FUNCTIONS/PROCEDURES
-- ===========================================
CREATE TABLE STUDENTS (
    STUDENTID SERIAL PRIMARY KEY,
    USERNAME VARCHAR(255) NOT NULL,
    CONSTRAINT FK_STUDENT_USER FOREIGN KEY (USERNAME)
        REFERENCES USERS(USERNAME)
        ON UPDATE CASCADE ON DELETE CASCADE,

    STUDID VARCHAR(20) NOT NULL,      -- code: S001, S002 (per account)
    STUDLNAME VARCHAR(255) NOT NULL,
    STUDFNAME VARCHAR(255) NOT NULL,
    STUDMNAME VARCHAR(255),
    STUDDOB DATE,
    STUDSEX VARCHAR(20) NOT NULL,
    STUDCONTACT VARCHAR(50) NOT NULL,
    MOTHERNAME VARCHAR(255) NOT NULL,
    MOTHERDOB DATE,
    FATHERNAME VARCHAR(255),
    FATHERDOB DATE,
    GUARDIANNAME VARCHAR(255),
    GUARDIANDOB DATE,
    CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT UNIQUE_STUD_PER_USER UNIQUE (USERNAME, STUDID)
);

CREATE OR REPLACE FUNCTION NEXT_STUDENT_CODE(P_USERNAME VARCHAR)
RETURNS VARCHAR
LANGUAGE PLPGSQL
AS $$
DECLARE
    LAST_CODE VARCHAR;
    LAST_NUM INT;
BEGIN
    SELECT STUDID INTO LAST_CODE
    FROM STUDENTS
    WHERE USERNAME = P_USERNAME
    ORDER BY STUDENTID DESC
    LIMIT 1;

    IF LAST_CODE IS NULL THEN
        RETURN 'S001';
    END IF;

    LAST_NUM := COALESCE(NULLIF(SUBSTRING(LAST_CODE FROM 2), ''), '0')::INT + 1;

    RETURN 'S' || LPAD(LAST_NUM::TEXT, 3, '0');
END;
$$;

CREATE OR REPLACE PROCEDURE ADD_STUDENT(
    P_USERNAME VARCHAR,
    P_STUDID VARCHAR,
    P_STUDLNAME VARCHAR,
    P_STUDFNAME VARCHAR,
    P_STUDMNAME VARCHAR,
    P_STUDDOB DATE,
    P_STUDSEX VARCHAR,
    P_STUDCONTACT VARCHAR,
    P_MOTHERNAME VARCHAR,
    P_MOTHERDOB DATE,
    P_FATHERNAME VARCHAR,
    P_FATHERDOB DATE,
    P_GUARDIANNAME VARCHAR,
    P_GUARDIANDOB DATE
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    INSERT INTO STUDENTS (
        USERNAME, STUDID, STUDLNAME, STUDFNAME, STUDMNAME,
        STUDDOB, STUDSEX, STUDCONTACT,
        MOTHERNAME, MOTHERDOB, FATHERNAME, FATHERDOB,
        GUARDIANNAME, GUARDIANDOB
    )
    VALUES (
        P_USERNAME, P_STUDID, P_STUDLNAME, P_STUDFNAME, P_STUDMNAME,
        P_STUDDOB, P_STUDSEX, P_STUDCONTACT,
        P_MOTHERNAME, P_MOTHERDOB, P_FATHERNAME, P_FATHERDOB,
        P_GUARDIANNAME, P_GUARDIANDOB
    );
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_STUDENT(
    P_USERNAME VARCHAR,
    P_STUDID VARCHAR,
    P_STUDLNAME VARCHAR,
    P_STUDFNAME VARCHAR,
    P_STUDMNAME VARCHAR,
    P_STUDDOB DATE,
    P_STUDSEX VARCHAR,
    P_STUDCONTACT VARCHAR,
    P_MOTHERNAME VARCHAR,
    P_MOTHERDOB DATE,
    P_FATHERNAME VARCHAR,
    P_FATHERDOB DATE,
    P_GUARDIANNAME VARCHAR,
    P_GUARDIANDOB DATE
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    UPDATE STUDENTS
    SET STUDLNAME = P_STUDLNAME,
        STUDFNAME = P_STUDFNAME,
        STUDMNAME = P_STUDMNAME,
        STUDDOB = P_STUDDOB,
        STUDSEX = P_STUDSEX,
        STUDCONTACT = P_STUDCONTACT,
        MOTHERNAME = P_MOTHERNAME,
        MOTHERDOB = P_MOTHERDOB,
        FATHERNAME = P_FATHERNAME,
        FATHERDOB = P_FATHERDOB,
        GUARDIANNAME = P_GUARDIANNAME,
        GUARDIANDOB = P_GUARDIANDOB
    WHERE USERNAME = P_USERNAME
      AND STUDID = P_STUDID;
END;
$$;

CREATE OR REPLACE PROCEDURE DELETE_STUDENT(
    P_USERNAME VARCHAR,
    P_STUDID VARCHAR
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    DELETE FROM STUDENTS
    WHERE USERNAME = P_USERNAME
      AND STUDID = P_STUDID;
END;
$$;


-- ===========================================
-- GUARDIANS TABLE + FUNCTIONS/PROCEDURES
-- ===========================================
CREATE TABLE GUARDIANS (
    GUARDIANID SERIAL PRIMARY KEY,
    STUDENTID INT NOT NULL REFERENCES STUDENTS(STUDENTID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    GUARDIANNAME VARCHAR(255) NOT NULL,
    GUARDIANDOB DATE,
    FACE_IMAGE_PATH TEXT,
    FACE_ENCODING BYTEA,
    CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE ADD_GUARDIAN(
    P_STUDENTID INT,
    P_NAME VARCHAR,
    P_DOB DATE,
    P_IMAGE_PATH TEXT,
    P_ENCODING BYTEA
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    INSERT INTO GUARDIANS (
        STUDENTID, GUARDIANNAME, GUARDIANDOB,
        FACE_IMAGE_PATH, FACE_ENCODING
    )
    VALUES (
        P_STUDENTID, P_NAME, P_DOB,
        P_IMAGE_PATH, P_ENCODING
    );
END;
$$;

CREATE OR REPLACE PROCEDURE UPDATE_GUARDIAN(
    P_GUARDIANID INT,
    P_NAME VARCHAR,
    P_DOB DATE,
    P_IMAGE_PATH TEXT,
    P_ENCODING BYTEA
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    UPDATE GUARDIANS
    SET GUARDIANNAME = P_NAME,
        GUARDIANDOB = P_DOB,
        FACE_IMAGE_PATH = P_IMAGE_PATH,
        FACE_ENCODING = P_ENCODING
    WHERE GUARDIANID = P_GUARDIANID;
END;
$$;

CREATE OR REPLACE PROCEDURE DELETE_GUARDIAN(P_GUARDIANID INT)
LANGUAGE PLPGSQL
AS $$
BEGIN
    DELETE FROM GUARDIANS WHERE GUARDIANID = P_GUARDIANID;
END;
$$;

DROP FUNCTION get_guardians_for_student(integer)

CREATE OR REPLACE FUNCTION GET_GUARDIANS_FOR_STUDENT(P_STUDENTID INT)
RETURNS TABLE(
    GUARDIANID INT,
    GUARDIANNAME VARCHAR,
    GUARDIANDOB DATE,
    FACE_IMAGE_PATH TEXT,
    FACE_ENCODING BYTEA,
    STUDID VARCHAR
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    RETURN QUERY
    SELECT
        G.GUARDIANID,
        G.GUARDIANNAME,
        G.GUARDIANDOB,
        G.FACE_IMAGE_PATH,
        G.FACE_ENCODING,
        S.STUDID
    FROM GUARDIANS G
    JOIN STUDENTS S ON S.STUDENTID = G.STUDENTID
    WHERE G.STUDENTID = P_STUDENTID
    ORDER BY G.GUARDIANID ASC;
END;
$$;


-- ===========================================
-- ATTENDANCE & LOGS TABLES + PROCEDURES
-- ===========================================
CREATE TABLE ATTENDANCE (
    ATTENDANCEID SERIAL PRIMARY KEY,
    STUDENTID INT NOT NULL REFERENCES STUDENTS(STUDENTID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    DATE DATE NOT NULL,
    DROPOFF_TIME TIMESTAMP,
    PICKUP_TIME TIMESTAMP,
    CONSTRAINT UNIQUE_STUDENT_DATE UNIQUE (STUDENTID, DATE)
);

CREATE TABLE LOGS (
    LOGID SERIAL PRIMARY KEY,
    STUDENTID INT NOT NULL REFERENCES STUDENTS(STUDENTID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    DATE DATE NOT NULL,
    STUDENTNAME VARCHAR(255) NOT NULL,
    DROPOFF_BY VARCHAR(255),
    PICKUP_BY VARCHAR(255),
    CONSTRAINT UNIQUE_LOG_PER_DAY UNIQUE (STUDENTID, DATE)
);

CREATE OR REPLACE PROCEDURE MARK_DROPOFF(
    P_STUDENTID INT,
    P_GUARDIAN_NAME VARCHAR,
    P_VERIFIED BOOLEAN
)
LANGUAGE PLPGSQL
AS $$
DECLARE
    TODAY DATE := CURRENT_DATE;
    V_STUDENTNAME VARCHAR(255);
BEGIN
    SELECT STUDLNAME || ', ' || STUDFNAME
    INTO V_STUDENTNAME
    FROM STUDENTS
    WHERE STUDENTID = P_STUDENTID;

    INSERT INTO ATTENDANCE (STUDENTID, DATE, DROPOFF_TIME)
    VALUES (P_STUDENTID, TODAY, NOW())
    ON CONFLICT (STUDENTID, DATE)
    DO UPDATE SET DROPOFF_TIME = EXCLUDED.DROPOFF_TIME;

    INSERT INTO LOGS (STUDENTID, DATE, STUDENTNAME, DROPOFF_BY)
    VALUES (
        P_STUDENTID,
        TODAY,
        V_STUDENTNAME,
        CASE WHEN P_VERIFIED THEN P_GUARDIAN_NAME ELSE 'UNVERIFIED GUARDIAN' END
    )
    ON CONFLICT (STUDENTID, DATE)
    DO UPDATE SET DROPOFF_BY = EXCLUDED.DROPOFF_BY;
END;
$$;

CREATE OR REPLACE PROCEDURE MARK_PICKUP(
    P_STUDENTID INT,
    P_GUARDIAN_NAME VARCHAR,
    P_VERIFIED BOOLEAN
)
LANGUAGE PLPGSQL
AS $$
DECLARE
    TODAY DATE := CURRENT_DATE;
    V_STUDENTNAME VARCHAR(255);
BEGIN
    SELECT STUDLNAME || ', ' || STUDFNAME
    INTO V_STUDENTNAME
    FROM STUDENTS
    WHERE STUDENTID = P_STUDENTID;

    INSERT INTO ATTENDANCE (STUDENTID, DATE, PICKUP_TIME)
    VALUES (P_STUDENTID, TODAY, NOW())
    ON CONFLICT (STUDENTID, DATE)
    DO UPDATE SET PICKUP_TIME = EXCLUDED.PICKUP_TIME;

    INSERT INTO LOGS (STUDENTID, DATE, STUDENTNAME, PICKUP_BY)
    VALUES (
        P_STUDENTID,
        TODAY,
        V_STUDENTNAME,
        CASE WHEN P_VERIFIED THEN P_GUARDIAN_NAME ELSE 'UNVERIFIED GUARDIAN' END
    )
    ON CONFLICT (STUDENTID, DATE)
    DO UPDATE SET PICKUP_BY = EXCLUDED.PICKUP_BY;
END;
$$;


DROP FUNCTION get_attendance_records(character varying,text)
-- ===========================================
-- REPORT FUNCTIONS
-- ===========================================
-- CREATE OR REPLACE FUNCTION GET_ATTENDANCE_RECORDS(
--     P_USERNAME VARCHAR,
--     P_SEARCH TEXT
-- )
-- RETURNS TABLE(
--     DATE DATE,
--     STUDID VARCHAR,
--     STUDENTNAME VARCHAR,
--     DROPOFF_BY VARCHAR,
--     PICKUP_BY VARCHAR,
--     DROPOFF_TIME TIMESTAMP,
--     PICKUP_TIME TIMESTAMP
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
--         A.DATE,
--         S.STUDID,
--         (S.STUDLNAME || ', ' || S.STUDFNAME)::VARCHAR,
--         L.DROPOFF_BY,
--         L.PICKUP_BY,
--         A.DROPOFF_TIME,
--         A.PICKUP_TIME
--     FROM ATTENDANCE A
--     JOIN LOGS L ON L.STUDENTID = A.STUDENTID AND L.DATE = A.DATE
--     JOIN STUDENTS S ON S.STUDENTID = A.STUDENTID
--     WHERE S.USERNAME = P_USERNAME
--       AND (
--             P_SEARCH IS NULL OR P_SEARCH = '' OR
--             S.STUDID ILIKE '%' || P_SEARCH || '%' OR
--             (S.STUDLNAME || ' ' || S.STUDFNAME) ILIKE '%' || P_SEARCH || '%' OR
--             A.DATE::TEXT ILIKE '%' || P_SEARCH || '%'
--       )
--     ORDER BY A.DATE DESC;
-- END;
-- $$;

-- CREATE OR REPLACE FUNCTION GET_LOGS_RECORDS(
--     P_USERNAME VARCHAR,
--     P_SEARCH TEXT
-- )
-- RETURNS TABLE(
--     DATE_DISPLAY TEXT,
--     STUDENTNAME VARCHAR,
--     DROPOFF_BY VARCHAR,
--     PICKUP_BY VARCHAR
-- )
-- LANGUAGE PLPGSQL
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         TO_CHAR(A.DROPOFF_TIME, 'YYYY-MM-DD HH24:MI:SS'),
--         L.STUDENTNAME,
--         L.DROPOFF_BY,
--         L.PICKUP_BY
--     FROM LOGS L
--     JOIN STUDENTS S ON S.STUDENTID = L.STUDENTID
--     LEFT JOIN ATTENDANCE A
--         ON A.STUDENTID = L.STUDENTID AND A.DATE = L.DATE
--     WHERE S.USERNAME = P_USERNAME
--       AND (
--             P_SEARCH IS NULL OR P_SEARCH = '' OR
--             L.STUDENTNAME ILIKE '%' || P_SEARCH || '%' OR
--             L.DROPOFF_BY ILIKE '%' || P_SEARCH || '%' OR
--             L.PICKUP_BY ILIKE '%' || P_SEARCH || '%' OR
--             L.DATE::TEXT ILIKE '%' || P_SEARCH || '%'
--       )
--     ORDER BY L.DATE DESC;
-- END;
-- $$;


-- DROP PROCEDURE add_guardian(integer,character varying,date,text,bytea)


-- DROP FUNCTION IF EXISTS get_guardians_for_student(VARCHAR);


CREATE OR REPLACE FUNCTION get_guardians_for_student(p_studentid INT)
RETURNS TABLE(
    guardianid INT,
    guardianname VARCHAR,
    guardiandob DATE,
    face_image_path TEXT,
    face_encoding BYTEA,
    studid VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        G.guardianid,
        G.guardianname,
        G.guardiandob,
        G.face_image_path,
        G.face_encoding,
        S.studid
    FROM guardians G
    JOIN students S ON S.studentid = G.studentid
    WHERE G.studentid = p_studentid
    ORDER BY G.guardianid ASC;
END;
$$;


-- DROP FUNCTION get_attendance_records(character varying,text)

-- CREATE OR REPLACE FUNCTION get_attendance_records(
--     p_username VARCHAR,
--     p_search TEXT
-- )
-- RETURNS TABLE(
--     date_display TEXT,
--     studid VARCHAR,
--     studentname VARCHAR,
--     dropoff_by VARCHAR,
--     pickup_by VARCHAR,
--     dropoff_time TIMESTAMP,
--     pickup_time TIMESTAMP
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         -- date + drop-off time
--         TO_CHAR(A.dropoff_time, 'YYYY-MM-DD HH24:MI:SS') AS date_display,

--         A.studid,
--         (S.studlname || ', ' || S.studfname)::VARCHAR AS studentname,
--         L.dropoff_by,
--         L.pickup_by,
--         A.dropoff_time,
--         A.pickup_time
--     FROM attendance A

--     -- FIRST join STUDENTS (link studid → studentid)
--     JOIN students S
--         ON S.studid = A.studid

--     -- THEN join LOGS by studentid + date
--     JOIN logs L
--         ON L.studentid = S.studentid
--        AND L.date = A.date

--     WHERE S.username = p_username
--       AND (
--             p_search IS NULL OR p_search = '' OR
--             A.studid ILIKE '%' || p_search || '%' OR
--             (S.studlname || ' ' || S.studfname) ILIKE '%' || p_search || '%' OR
--             A.date::TEXT ILIKE '%' || p_search || '%'
--       )

--     ORDER BY A.date DESC;
-- END;
-- $$;




-- CREATE OR REPLACE FUNCTION get_attendance_records(
--     p_username VARCHAR,
--     p_search TEXT
-- )
-- RETURNS TABLE(
--     date_display TEXT,
--     studid VARCHAR,
--     studentname VARCHAR,
--     dropoff_by VARCHAR,
--     pickup_by VARCHAR,
--     dropoff_time TIMESTAMP,
--     pickup_time TIMESTAMP
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         -- Show date + dropoff time
--         TO_CHAR(A.dropoff_time, 'YYYY-MM-DD HH24:MI:SS') AS date_display,

--         S.studid,  -- <-- PERFECT: comes from students table
--         (S.studlname || ', ' || S.studfname)::VARCHAR AS studentname,
--         L.dropoff_by,
--         L.pickup_by,
--         A.dropoff_time,
--         A.pickup_time
--     FROM attendance A

--     -- join via studentid (INT)
--     JOIN students S
--         ON S.studentid = A.studentid

--     JOIN logs L
--         ON L.studentid = S.studentid
--        AND L.date = A.date

--     WHERE S.username = p_username
--       AND (
--             p_search IS NULL OR p_search = '' OR
--             S.studid ILIKE '%' || p_search || '%' OR
--             (S.studlname || ' ' || S.studfname) ILIKE '%' || p_search || '%' OR
--             A.date::TEXT ILIKE '%' || p_search || '%'
--       )

--     ORDER BY 
--         L.date DESC,
--         COALESCE(A.pickup_time, A.dropoff_time) DESC;
-- END;
-- $$;


-- DROP FUNCTION get_logs_records(character varying,text)

-- CREATE OR REPLACE FUNCTION get_logs_records(
--     p_username VARCHAR,
--     p_search TEXT
-- )
-- RETURNS TABLE(
--     date_display TEXT,
--     studentname VARCHAR,
--     activity_log TEXT
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         TO_CHAR(L.date, 'YYYY-MM-DD') AS date_display,

--         S.studlname || ', ' || S.studfname AS studentname,

--         (
--             'Drop-off: ' ||
--             COALESCE(
--                 CASE 
--                     WHEN L.dropoff_by IS NOT NULL THEN 
--                         TO_CHAR(A.dropoff_time, 'HH12:MI AM') || ' — by ' || L.dropoff_by
--                     ELSE
--                         'Not yet recorded'
--                 END,
--             'Not yet recorded'
--             )
--             || E'\n' ||
--             'Pick-up: ' ||
--             COALESCE(
--                 CASE
--                     WHEN L.pickup_by IS NOT NULL THEN 
--                         TO_CHAR(A.pickup_time, 'HH12:MI AM') || ' — by ' || L.pickup_by
--                     ELSE
--                         'Not yet recorded'
--                 END,
--             'Not yet recorded'
--             )
--         ) AS activity_log

--     FROM logs L
--     JOIN students S
--         ON S.studentid = L.studentid
--     LEFT JOIN attendance A
--         ON A.studentid = L.studentid
--        AND A.date = L.date

--     WHERE S.username = p_username
--       AND (
--             p_search IS NULL OR p_search = '' OR
--             S.studid ILIKE '%' || p_search || '%' OR
--             S.studlname ILIKE '%' || p_search || '%' OR
--             S.studfname ILIKE '%' || p_search || '%' OR
--             L.date::TEXT ILIKE '%' || p_search || '%'
--       )

--     ORDER BY L.date DESC;
-- END;
-- $$;



-- DROP FUNCTION get_logs_records(character varying,text) 


-- CREATE OR REPLACE FUNCTION get_logs_records(
--     p_username VARCHAR,
--     p_search TEXT
-- )
-- RETURNS TABLE(
--     date_display TEXT,
--     studentname VARCHAR,
--     dropoff_by VARCHAR,
--     dropoff_time TIMESTAMP,
--     pickup_by VARCHAR,
--     pickup_time TIMESTAMP
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         TO_CHAR(L.date, 'YYYY-MM-DD') AS date_display,

--         (S.studlname || ', ' || S.studfname)::VARCHAR AS studentname,

--         L.dropoff_by,
--         A.dropoff_time,

--         L.pickup_by,
--         A.pickup_time
--     FROM logs L

--     JOIN students S
--         ON S.studentid = L.studentid

--     LEFT JOIN attendance A
--         ON A.studentid = S.studentid
--        AND A.date = L.date

--     WHERE S.username = p_username
--       AND (
--             p_search IS NULL OR p_search = '' OR
--             L.dropoff_by ILIKE '%' || p_search || '%' OR
--             L.pickup_by ILIKE '%' || p_search || '%' OR
--             (S.studlname || ' ' || S.studfname) ILIKE '%' || p_search || '%' OR
--             L.date::TEXT ILIKE '%' || p_search || '%'
--       )
--     ORDER BY 
--         L.date DESC,
--         COALESCE(A.pickup_time, A.dropoff_time) DESC;
-- END;
-- $$;






CREATE OR REPLACE FUNCTION get_attendance_records(
    p_username VARCHAR,
    p_search TEXT
)
RETURNS TABLE(
    date_display TEXT,
    studid VARCHAR,
    studentname VARCHAR,
    dropoff_by VARCHAR,
    pickup_by VARCHAR,
    dropoff_time TIMESTAMP,
    pickup_time TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        -- date + dropoff time
        TO_CHAR(A.dropoff_time, 'YYYY-MM-DD HH24:MI:SS') AS date_display,

        S.studid,  -- ✔ studid comes from STUDENTS table
        (S.studlname || ', ' || S.studfname)::VARCHAR AS studentname,
        L.dropoff_by,
        L.pickup_by,
        A.dropoff_time,
        A.pickup_time
    FROM attendance A

    -- ✔ Correct join (use studentid)
    JOIN students S
        ON S.studentid = A.studentid

    JOIN logs L
        ON L.studentid = S.studentid
       AND L.date = A.date

    WHERE S.username = p_username
      AND (
            p_search IS NULL OR p_search = '' OR
            S.studid ILIKE '%' || p_search || '%' OR
            (S.studlname || ' ' || S.studfname) ILIKE '%' || p_search || '%' OR
            A.date::TEXT ILIKE '%' || p_search || '%'
      )

    ORDER BY 
        L.date DESC,
        COALESCE(A.pickup_time) DESC;
END;
$$;






CREATE OR REPLACE FUNCTION get_logs_records(
    p_username VARCHAR,
    p_search TEXT
)
RETURNS TABLE(
    date_display TEXT,
    studentname VARCHAR,
    dropoff_by VARCHAR,
    dropoff_time TIMESTAMP,
    pickup_by VARCHAR,
    pickup_time TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        TO_CHAR(L.date, 'YYYY-MM-DD') AS date_display,

        (S.studlname || ', ' || S.studfname)::VARCHAR AS studentname,

        L.dropoff_by,
        A.dropoff_time,

        L.pickup_by,
        A.pickup_time
    FROM logs L

    JOIN students S
        ON S.studentid = L.studentid

    LEFT JOIN attendance A
        ON A.studentid = S.studentid
       AND A.date = L.date

    WHERE S.username = p_username
      AND (
            p_search IS NULL OR p_search = '' OR
            L.dropoff_by ILIKE '%' || p_search || '%' OR
            L.pickup_by ILIKE '%' || p_search || '%' OR
            (S.studlname || ' ' || S.studfname) ILIKE '%' || p_search || '%' OR
            L.date::TEXT ILIKE '%' || p_search || '%'
      )
    ORDER BY 
        L.date DESC,
        COALESCE(A.pickup_time, A.dropoff_time) DESC;
END;
$$;
