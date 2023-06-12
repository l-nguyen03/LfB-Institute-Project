import dlib
import cv2 as cv
import face_recognition as fr
import numpy as np
import time
from datetime import datetime
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(dir_path, "shape_predictor_81_face_landmarks.dat")
jpg_dir_path = os.path.join(dir_path, "faces")

# Initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()

# Path for shape_predictor
predictor = dlib.shape_predictor(model_path)

# Load the known face image and encode it
student_img = [fr.load_image_file(os.path.join(jpg_dir_path, jpg_file)) for jpg_file in os.listdir(jpg_dir_path) if
               ".jpg" in jpg_file]

# List of known face encodings
known_face_encoding = [fr.face_encodings(student_image)[0] for student_image in student_img]
known_names = ["Student"]  # List of known names


def camera_monitor(img):
    unknown_face_start_time = None

    # Convert the image to grayscale for better face detection
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Check if more faces or no face present
    if len(faces) > 1:
        message = "More than one face detected!"
        print(message)
        unknown_face_start_time = time.time()
        unknown_face_start_time = datetime.fromtimestamp(unknown_face_start_time)
        log_message(message, unknown_face_start_time)
        return True, img, unknown_face_start_time
    elif len(faces) == 0:
        message = "Face out of frame!"
        print(message)
        unknown_face_start_time = time.time()
        unknown_face_start_time = datetime.fromtimestamp(unknown_face_start_time)
        log_message(message, unknown_face_start_time)
        return True, img, unknown_face_start_time

    # If only one face present then proceed to identity check
    for face in faces:
        landmarks = predictor(gray, face)

    # Print messages
    if unknown_face_start_time is not None:
        message = "Unknown face"
        print(message)
        log_message(message, unknown_face_start_time)
        return True, img, unknown_face_start_time

    return False, img, unknown_face_start_time


def log_message(message, timestamp):
    log_dir = os.path.join(dir_path, 'frame_evidence')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, 'log.txt')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{timestamp}: {message}\n')
