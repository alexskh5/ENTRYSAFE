CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    userID          SERIAL PRIMARY KEY,
    username        VARCHAR(255) NOT NULL UNIQUE,
    userpassword    TEXT NOT NULL,
    userHomepass    VARCHAR(20),
    createdAt       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- SIGNUP USER
CREATE OR REPLACE PROCEDURE signup_user(
    p_username VARCHAR,
    p_password VARCHAR,
    p_homepass VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (username, userpassword, userHomepass)
    VALUES (
        p_username,
        crypt(p_password, gen_salt('bf')),
        crypt(p_homepass, gen_salt('bf'))
    );
END;
$$;

-- LOGIN FUNCTION
CREATE OR REPLACE FUNCTION login_user(
    p_username VARCHAR,
    p_password VARCHAR
)
RETURNS TABLE(
    userID INT,
    username VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.userID, u.username
    FROM users u
    WHERE LOWER(u.username) = LOWER(p_username)
      AND u.userPassword = crypt(p_password, u.userPassword);
END;
$$ LANGUAGE plpgsql;



select * from users;




ALTER TABLE users
ALTER COLUMN userHomepass TYPE TEXT;

UPDATE users
SET userHomepass = crypt(userHomepass, gen_salt('bf'))
WHERE username = 'admin';

