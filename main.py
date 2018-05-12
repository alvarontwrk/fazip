import face_recognition
import cv2
from time import clock
from sys import exit

print("START")


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


faces = get_face_encoding()
facescomp = get_face_encoding()

match = face_recognition.compare_faces([faces], facescomp)
print("MATCH? {}".format(match[0]))

print("END {}".format(clock()))
