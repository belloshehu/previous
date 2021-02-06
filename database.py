import sqlite3

def make_connection():
    connection = sqlite3.connect('previous_lessons.sqlite')
    cursor = connection.cursor()
    return cursor, connection

def create_tables():
    ''' Creates user authentication table.'''
    cursor, connection = make_connection()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Auth
            (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                username TEXT UNIQUE, 
                password TEXT
             )'''
    )
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Course
            (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                name TEXT
             )'''
    )
    

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Tutor
            (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                contact TEXT,
                UNIQUE(full_name, contact)
             )'''
    )


    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Lesson
            (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                date TEXT
             )'''
    )
    connection.commit()
    

def add_course(title, name):
    cursor, connection = make_connection()
    cursor.execute('''INSERT INTO Course (title, name) VALUES(?,?)''', (title, name, ))
    connection.commit()
    return cursor


def add_tutor(full_name, contact):
    cursor, connection = make_connection()
    cursor.execute('''INSERT INTO Tutor (full_name, contact) VALUES(?,?)''', (full_name, contact, ))
    connection.commit()
    return cursor


def add_lesson(name, description, date_time):
    cursor, connection = make_connection()
    cursor.execute(
        '''INSERT INTO Lesson (title, description, date) VALUES(?, ?, ?)''', 
        (name, description, date_time,)
    )
    connection.commit()
    return cursor

