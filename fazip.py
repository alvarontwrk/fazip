import face_recognition
import cv2
from time import clock
from sys import exit
import numpy as np
import pymysql
import subprocess
import zipfile


def get_face_encoding():
    faces = []
    video_capture = cv2.VideoCapture(0)
    start, current = clock(), 0
    it = 0

    while not faces and current < 5:
        it += 1
        print("LAP {}".format(it))
        current = clock() - start
        ret, frame = video_capture.read()
        faces = face_recognition.face_encodings(frame)

        if len(faces) > 1:
            print("Please, stay alone in front of the camera")

    try:
        return faces[0]
    except Exception:
        print("EXCEPTION: Face not found! :(")
        exit()


def connect_to_db(user, password, host="localhost"):
    return pymysql.connect(host, user, password)


def execute_db(database, sentence, get_info=False, commit=False):
    cursor = database.cursor()

    try:
        cursor.execute(sentence)
        if commit:
            database.commit()
        if get_info:
            return cursor.fetchall()
    except Exception as e:
        database.rollback()
        print_error_db(e)


def create_db(database):
    sentence = 'CREATE DATABASE fazip'
    execute_db(database, sentence)


def print_error_db(exception):
    errors = {1007: 'ERROR: Database already exists!',
              1050: 'ERROR: Table already exists!',
              1062: 'ERROR: User already registered!'}
    key = exception.args[0]
    if key in errors:
        print(errors[exception.args[0]])
    else:
        print('--> {}'.format(exception))


def exists_db(database):
    result = execute_db(database, """SELECT SCHEMA_NAME FROM
                          INFORMATION_SCHEMA.SCHEMATA
                          WHERE SCHEMA_NAME = 'fazip'""", get_info=True)

    return len(result) == 1


def use_db(database):
    sentence = 'USE fazip'
    execute_db(database, sentence)


def create_table_db(database):
    use_db(database)
    sentence = """CREATE TABLE Faces(
                Name CHAR(20) NOT NULL,
                Encoding TEXT NOT NULL,
                PRIMARY KEY(Name))"""
    execute_db(database, sentence)
    sentence = """CREATE TABLE Credentials(
                TheGroup CHAR(20) NOT NULL,
                Password TEXT NOT NULL,
                PRIMARY KEY(TheGroup))"""
    execute_db(database, sentence)


def show_table_db(database):
    use_db(database)
    sentence = 'SELECT * FROM Faces'
    print(execute_db(database, sentence, True))


def add_user_db(database, name):
    use_db(database)
    encoding = get_face_encoding()
    sentence = 'INSERT INTO Faces VALUES("{}", "{}")'.format(name, encoding)
    execute_db(database, sentence, commit=True)


def set_password_zip(database, password):
    use_db(database)
    sentence = 'SELECT COUNT(*) FROM Credentials'
    exists = execute_db(database, sentence, get_info=True)[0][0] == 1
    if not exists:
        sentence = 'INSERT INTO Credentials VALUEs(\
                    "Master","{}")'.format(password)
    else:
        sentence = 'UPDATE Credentials SET Password = "{}"\
                    WHERE TheGroup = "Master"'.format(password)
    execute_db(database, sentence, commit=True)


def get_password_zip(database):
    use_db(database)
    sentence = 'SELECT Password FROM Credentials WHERE TheGroup = "Master"'
    reponse = execute_db(database, sentence, get_info=True)[0][0]
    return reponse


def remove_user_db(database, name):
    use_db(database)
    sentence = 'DELETE FROM Faces WHERE Name = "{}"'.format(name)
    execute_db(database, sentence, commit=True)


def modify_user_db(database, name):
    use_db(database)
    encoding = get_face_encoding()
    sentence = 'UPDATE Faces SET Encoding = "{}"\
                WHERE Name = "{}"'.format(encoding, name)
    execute_db(database, sentence, commit=True)


def get_encoding_db(database):
    use_db(database)
    sentence = 'SELECT Encoding FROM Faces'
    reponse = execute_db(database, sentence, get_info=True)
    faces = []

    for array in reponse:
        array = array[0][1:-1]
        a = np.fromstring(array, sep=' ')
        faces.append(a)

    return faces


def face_in_db(database, face):
    faces = get_encoding_db(database)
    match = face_recognition.compare_faces(faces, face)
    return True in match


def zip_files(database, zipname, files):
    password = get_password_zip(database)
    command = '7z a -p{} -y {} {}'.format(password, zipname, files)
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        print("{} created successfully!".format(zipname))
    except Exception as e:
        print(e)


def unzip_files(database, zipname):
    face = get_face_encoding()
    if face_in_db(database, face):
        password = str.encode(get_password_zip(database))
        with zipfile.ZipFile(zipname) as myzip:
            try:
                myzip.extractall(pwd=password)
                print('{} extracted successfully!'.format(zipname))
            except Exception as e:
                print(e)
    else:
        print('ERROR: User not registered in the database!')


if __name__ == '__main__':
    db = connect_to_db('root', 'toor')
    # create_db(db)
    # create_table_db(db)
    # set_password_zip(db, 'testing_pass')
    # add_user_db(db, 'Alvaro')
    # modify_user_db(db, 'Alvaro')
    # remove_user_db(db, 'Alvaro')
    # show_table_db(db)
    # get_encoding_db(db)
    # print(face_in_db(db, get_face_encoding()))
    # print(get_password_zip(db))
    # zip_files(db, 'zipfile.zip', 'test2zip anothertest.txt')
    unzip_files(db, 'zipfile.zip')
    db.close()

    '''
    faces = get_face_encoding()


    facescomp = get_face_encoding()

    match = face_recognition.compare_faces([faces], facescomp)
    print("MATCH? {}".format(match[0]))
    print("SIZE: {}".format(len(faces)))
    print("SIZE: {}".format(len(faces.tobytes())))

    print("END {}".format(clock()))
    '''
