DROP TABLE IF EXISTS users CASCADE;


CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    userid SERIAL PRIMARY KEY,

    username VARCHAR(255) NOT NULL UNIQUE,
    userpassword TEXT NOT NULL,
    userhomepass TEXT,

    q1 TEXT NOT NULL,
    a1 TEXT NOT NULL,
    q2 TEXT NOT NULL,
    a2 TEXT NOT NULL,

    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE OR REPLACE PROCEDURE signup_user(
    p_username VARCHAR,
    p_password VARCHAR,
    p_homepass VARCHAR,
    p_q1 TEXT,
    p_a1 TEXT,
    p_q2 TEXT,
    p_a2 TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (
        username, userpassword, userhomepass,
        q1, a1, q2, a2
    )
    VALUES (
        p_username,
        crypt(p_password, gen_salt('bf')),
        CASE WHEN p_homepass IS NULL OR p_homepass = ''
             THEN NULL
             ELSE crypt(p_homepass, gen_salt('bf'))
        END,
        p_q1,
        crypt(lower(p_a1), gen_salt('bf')),
        p_q2,
        crypt(lower(p_a2), gen_salt('bf'))
    );
END;
$$;




CREATE OR REPLACE FUNCTION login_user(
    p_username VARCHAR,
    p_password VARCHAR
)
RETURNS TABLE(
    userid INT,
    username VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT u.userid, u.username
    FROM users u
    WHERE LOWER(u.username) = LOWER(p_username)
      AND u.userpassword = crypt(p_password, u.userpassword);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_security_questions(p_username TEXT)
RETURNS TABLE(q1 TEXT, q2 TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT u.q1, u.q2
    FROM users u
    WHERE LOWER(username) = LOWER(p_username);
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION verify_security_answers(
    p_username TEXT,
    p_a1 TEXT,
    p_a2 TEXT
)
RETURNS BOOLEAN
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM users
        WHERE LOWER(username) = LOWER(p_username)
          AND a1 = crypt(lower(p_a1), a1)
          AND a2 = crypt(lower(p_a2), a2)
    );
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE update_user_password(
    p_username TEXT,
    p_new_password TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET userpassword = crypt(p_new_password, gen_salt('bf'))
    WHERE LOWER(username) = LOWER(p_username);
END;
$$;




DELETE FROM users
WHERE username = 'admin';


SELECT * FROM users;



CREATE OR REPLACE FUNCTION verify_home_pass(
    p_username TEXT,
    p_homepass TEXT
)
RETURNS BOOLEAN
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM users
        WHERE LOWER(username) = LOWER(p_username)
          AND userhomepass = crypt(p_homepass, userhomepass)
    );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_home_pass(
    p_username TEXT,
    p_new_homepass TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET userhomepass = crypt(p_new_homepass, gen_salt('bf'))
    WHERE LOWER(username) = LOWER(p_username);
END;
$$;









DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    studentid SERIAL PRIMARY KEY,

    -- FK to users table
    username VARCHAR(255) NOT NULL,
    CONSTRAINT fk_student_user
        FOREIGN KEY (username)
        REFERENCES users(username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    studID VARCHAR(20) NOT NULL UNIQUE,  -- S001, S002, etc.

    studLname VARCHAR(255) NOT NULL,
    studFname VARCHAR(255) NOT NULL,
    studMname VARCHAR(255),

    studDOB DATE,
    studSex VARCHAR(20) NOT NULL,

    studContact VARCHAR(50) NOT NULL,

    motherName VARCHAR(255) NOT NULL,
    motherDOB DATE,

    fatherName VARCHAR(255),
    fatherDOB DATE,

    guardianName VARCHAR(255),
    guardianDOB DATE,

    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE OR REPLACE FUNCTION next_student_code(p_username VARCHAR)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE
    last_code VARCHAR;
    last_num  INT;
BEGIN
    SELECT studID
    INTO last_code
    FROM students
    WHERE username = p_username
    ORDER BY studentid DESC
    LIMIT 1;

    IF last_code IS NULL THEN
        RETURN 'S001';
    END IF;

    -- get numeric part, assume format 'Snnn'
    last_num := COALESCE(NULLIF(SUBSTRING(last_code FROM 2), ''), '0')::INT;
    last_num := last_num + 1;

    RETURN 'S' || LPAD(last_num::TEXT, 3, '0');
END;
$$;





CREATE OR REPLACE PROCEDURE add_student(
    p_username      VARCHAR,
    p_studID        VARCHAR,
    p_studLname     VARCHAR,
    p_studFname     VARCHAR,
    p_studMname     VARCHAR,
    p_studDOB       DATE,
    p_studSex       VARCHAR,
    p_studContact   VARCHAR,
    p_motherName    VARCHAR,
    p_motherDOB     DATE,
    p_fatherName    VARCHAR,
    p_fatherDOB     DATE,
    p_guardianName  VARCHAR,
    p_guardianDOB   DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO students (
        username,
        studID,
        studLname, studFname, studMname,
        studDOB, studSex,
        studContact,
        motherName, motherDOB,
        fatherName, fatherDOB,
        guardianName, guardianDOB
    ) VALUES (
        p_username,
        p_studID,
        p_studLname, p_studFname, p_studMname,
        p_studDOB, p_studSex,
        p_studContact,
        p_motherName, p_motherDOB,
        p_fatherName, p_fatherDOB,
        p_guardianName, p_guardianDOB
    );
END;
$$;



select * from students;


CREATE OR REPLACE PROCEDURE update_student(
    p_studID        VARCHAR,
    p_studLname     VARCHAR,
    p_studFname     VARCHAR,
    p_studMname     VARCHAR,
    p_studDOB       DATE,
    p_studSex       VARCHAR,
    p_studContact   VARCHAR,
    p_motherName    VARCHAR,
    p_motherDOB     DATE,
    p_fatherName    VARCHAR,
    p_fatherDOB     DATE,
    p_guardianName  VARCHAR,
    p_guardianDOB   DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE students
    SET
        studLname = p_studLname,
        studFname = p_studFname,
        studMname = p_studMname,
        studDOB = p_studDOB,
        studSex = p_studSex,
        studContact = p_studContact,
        motherName = p_motherName,
        motherDOB = p_motherDOB,
        fatherName = p_fatherName,
        fatherDOB = p_fatherDOB,
        guardianName = p_guardianName,
        guardianDOB = p_guardianDOB
    WHERE studID = p_studID;
END;
$$;









DROP TABLE IF EXISTS guardians CASCADE;

CREATE TABLE guardians (
    guardianid SERIAL PRIMARY KEY,

    studid VARCHAR(20) NOT NULL,
    FOREIGN KEY (studid)
        REFERENCES students(studID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    guardianname VARCHAR(255) NOT NULL,
    guardiandob DATE,
    
    face_image_path TEXT,
    face_encoding BYTEA,

    createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);






CREATE OR REPLACE PROCEDURE add_guardian(
    p_studid        INT,
    p_guardianname  VARCHAR,
    p_guardiandob   DATE,
    p_image_path    TEXT,
    p_face_encoding BYTEA
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO guardians(
        studid,
        guardianname,
        guardiandob,
        image_path,
        face_encoding
    )
    VALUES (
        p_studid,
        p_guardianname,
        p_guardiandob,
        p_image_path,
        p_face_encoding
    );
END;
$$;






CREATE OR REPLACE PROCEDURE update_guardian(
    p_guardianid    INT,
    p_guardianname  VARCHAR,
    p_guardiandob   DATE,
    p_image_path    TEXT,
    p_face_encoding BYTEA
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE guardians
    SET
        guardianname = p_guardianname,
        guardiandob = p_guardiandob,
        image_path = p_image_path,
        face_encoding = p_face_encoding
    WHERE guardianid = p_guardianid;
END;
$$;

