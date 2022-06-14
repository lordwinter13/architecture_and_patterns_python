PRAGMA foreign_keys = off;

BEGIN TRANSACTION;
    DROP TABLE IF EXISTS categories;
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name VARCHAR (255)
    );

    DROP TABLE IF EXISTS courses;
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        category INTEGER NOT NULL,
        name VARCHAR (255),
        place VARCHAR (255),
        type VARCHAR (255)
    );

    DROP TABLE IF EXISTS students;
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        name VARCHAR (255)
    );

    DROP TABLE IF EXISTS enrolled_students;
    CREATE TABLE enrolled_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL
    );
COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
