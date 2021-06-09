--
-- File generated with SQLiteStudio v3.3.3 on Wed Jun 9 10:13:15 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
-- Table: interest
DROP TABLE IF EXISTS interest;
CREATE TABLE interest (
    id VARCHAR (30) PRIMARY KEY,
    description VARCHAR (20) NOT NULL
);
-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    username VARCHAR (30) PRIMARY KEY,
    password VARCHAR (30) NOT NULL,
    first_name VARCHAR (30) NOT NULL,
    last_name VARCHAR (30) NOT NULL,
    email TEXT (30) NOT NULL,
    nationality VARCHAR (30) NOT NULL,
    mobile TEXT (20),
    about TEXT (200),
    last_login DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
-- Table: user_interest
DROP TABLE IF EXISTS user_interest;
CREATE TABLE user_interest (
    user_username VARCHAR (30) REFERENCES user (username) NOT NULL,
    interest_id INTEGER REFERENCES interest (id) NOT NULL
);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
