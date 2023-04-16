import cv2
import numpy
from PIL import Image
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def Detection(img):
    img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.301, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (100, 200, 250), 2)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
