--
-- File generated with SQLiteStudio v3.3.3 on Mon Jun 7 16:18:30 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    username VARCHAR (30) PRIMARY KEY,
    password VARCHAR (30) NOT NULL,
    first_name VARCHAR (30) NOT NULL,
    last_name VARCHAR (30) NOT NULL,
    email TEXT (30) NOT NULL,
    mobile TEXT (20),
    about TEXT (200),
    last_login DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL
);
COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
