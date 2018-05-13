import face_recognition
import cv2
from time import clock
from sys import exit
# import numpy as np
import pymysql


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


def execute_db(database, sentence, get_info=False):
    cursor = database.cursor()
    try:
        cursor.execute(sentence)
        if get_info:
            return cursor.fetchall()
    except Exception as e:
        print(e)


def create_db(database):
    sentence = 'CREATE DATABASE fazip'
    execute_db(database, sentence)


def exists_db(database):
    result = execute_db(database, """SELECT SCHEMA_NAME FROM
                          INFORMATION_SCHEMA.SCHEMATA
                          WHERE SCHEMA_NAME = 'fazip'""", True)

    return len(result) == 1


def create_table_db(database):
    sentence = 'USE fazip'
    execute_db(database, sentence)
    sentence = """CREATE TABLE access(
                NAME CHAR(20) NOT NULL,
                ENCODING TEXT NOT NULL)"""
    execute_db(database, sentence)


if __name__ == '__main__':
    db = connect_to_db('root', 'toor')
    create_db(db)
    create_table_db(db)

    '''
    faces = get_face_encoding()


    a = faces.tobytes()
    print(type(a))
    b = np.frombuffer(a)
    print(type(b))
    print(np.frombuffer(a))

    facescomp = get_face_encoding()

    match = face_recognition.compare_faces([faces], facescomp)
    print("MATCH? {}".format(match[0]))
    print("SIZE: {}".format(len(faces)))
    print("SIZE: {}".format(len(faces.tobytes())))

    print("END {}".format(clock()))
    '''
