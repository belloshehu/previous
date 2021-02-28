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
                course INTEGER,
                UNIQUE(full_name, contact)
             )'''
    )


    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Lesson
            (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                date TEXT,
                course INTEGER
             )'''
    )
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Course_lesson
            (
                id INTEGER PRIMARY KEY,
                course INTEGER,
                lesson INTEGER
            )
        '''
    )
    connection.commit()
    

def add_course(title, name):
    cursor, connection = make_connection()
    cursor.execute('''INSERT INTO Course (title, name) VALUES(?,?)''', (title, name, ))
    connection.commit()
    return cursor


def add_tutor(full_name, contact, course_detail):
    cursor, connection = make_connection()
    # get the course instance from database
    course = get_course(course_detail.text, course_detail.secondary_text)
    cursor.execute('''INSERT INTO Tutor (full_name, contact, course) VALUES(?,?,?)''', (full_name, contact, course[0], ))
    connection.commit()
    return cursor


def add_lesson(name, description, date_time, course_detail):
    cursor, connection = make_connection()
    try:
        course = get_course(course_detail.text, course_detail.secondary_text)
        cursor.execute(
            '''INSERT INTO Lesson (title, description, date, course) VALUES(?, ?, ?, ?)''', 
            (name, description, date_time, course[0],)
        )
    except Exception as e:
        print(e)
    connection.commit()
    return cursor


def get_lessons():
    cursor, connection = make_connection()
    cursor.execute('''SELECT * FROM Lesson''')
    connection.commit()
    return cursor.fetchall()


def get_lesson(title, description, course_detail):
    cursor, connection = make_connection()
    # get the course instance from database
    try:
        course = get_course(course_detail.text, course_detail.secondary_text)
        cursor.execute(
            '''SELECT * FROM Lesson WHERE title=? AND description=? AND course=?''',
            (title, description, course[0],)
        )
    except Exception as e:
        print(e)
    connection.commit()
    return cursor.fetchone()


def update_lesson(title, description, date, id):
    cursor, connection = make_connection()
    cursor.execute(
        '''UPDATE Lesson SET title=?, description=?, date=? WHERE id=?''',
        (title, description, date, id)
    )
    connection.commit()

def delete_lesson(id):
    cursor, connection = make_connection()
    cursor.execute(''' DELETE FROM Lesson WHERE id=?''', (id,))
    connection.commit()

def get_course_lessons(course_id):
    cursor, connection = make_connection()
    # get the course instance from database
    try:
        #course = get_course(course_detail.text, course_detail.secondary_text)
        cursor.execute('''SELECT * FROM Lesson WHERE course=?''', (course_id,))
    except Exception as e:
        print(e)
    connection.commit()
    return cursor.fetchall()


def get_courses():
    cursor, connection = make_connection()
    cursor.execute('''SELECT * FROM Course''')
    connection.commit()
    return cursor.fetchall()


def get_tutors():
    cursor, connection = make_connection()
    cursor.execute('''SELECT * FROM Tutor''')
    connection.commit()
    return cursor.fetchall()


def get_course_tutors(course_id):
    cursor, connection = make_connection()
    # get the course instance from database
    #course = get_course(course_detail.text, course_detail.secondary_text)
    try:
        cursor.execute('''SELECT * FROM Tutor WHERE course=?''', (course_id,))
    except Exception as e:
        print(e)

    connection.commit()
    return cursor.fetchall()

def delete_tutor(id):
    cursor, connection = make_connection()
    cursor.execute(''' DELETE FROM Tutor WHERE id=?''', (id,))
    connection.commit()


def update_tutor(full_name, contact, item_id):
    cursor, connection = make_connection()
    cursor.execute(
        ''' UPDATE Tutor SET full_name=?, contact=? WHERE id=?''', 
        (full_name, contact, item_id)
    )
    connection.commit()


def get_tutor(full_name, contact, course_detail):
    cursor, connection = make_connection()
    course = get_course(course_detail.text, course_detail.secondary_text)
    cursor.execute(
        '''SELECT * FROM Tutor WHERE full_name=? AND contact=? AND course=?''',
        (full_name, contact, course[0],)
    )
    connection.commit()
    return cursor.fetchone()


def get_course(title, name):
    cursor, connection = make_connection()
    cursor.execute('''SELECT * FROM Course WHERE title=? AND name=?''', (title, name,))
    connection.commit()
    return cursor.fetchone()

def update_course(title, name, id):
    cursor, connection = make_connection()
    cursor.execute(
        '''UPDATE Course SET title=?, name=? WHERE id=?''',
        (title, name, id)
    )
    connection.commit()

def delete_course(id):
    cursor, connection = make_connection()
    # delete course with a given id
    cursor.execute(''' DELETE FROM Course WHERE id=? ''', (id,))
    # delete the course tutors and lessons too
    cursor.execute(''' DELETE FROM Tutor WHERE course=? ''', (id,))
    cursor.execute(''' DELETE FROM Lesson WHERE course=? ''', (id,))
    connection.commit()
    return cursor.fetchone()
