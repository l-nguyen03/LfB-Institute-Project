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
known_names = [jpg_file.split(".jpg")[0] for jpg_file in os.listdir(jpg_dir_path) if ".jpg" in jpg_file]  # List of known names


"""
The function uses an input image frame and detect 2 things:
How many faces there are in the input frame and 
whether the identity of the test taker match the reference image
It then returns a boolean value indicating cheating and if cheating is detected
return the frame as evidence and a brief description.
"""
def camera_monitor(img, matrikelnr):
    unknown_face_start_time = None

    # Convert the image to grayscale for better face detection
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Check if more faces or no face present
    if len(faces) > 1:
        message = "More than one face detected!"
        print(message)
        unknown_face_start_time = time.time()
        unknown_face_start_time = str(datetime.fromtimestamp(unknown_face_start_time))
        descriptor = f"{matrikelnr}: {message} at {unknown_face_start_time}"
        for face in faces:
            x, y, width, height = face.left(), face.top(), face.width(), face.height()
            cv.rectangle(img, (x, y), (x + width, y + height), color=(0, 0, 255), thickness=5)
        return True, img, descriptor
    elif len(faces) == 0:
        message = "Face out of frame!"
        print(message)
        unknown_face_start_time = time.time()
        unknown_face_start_time = datetime.fromtimestamp(unknown_face_start_time)
        descriptor = f"{matrikelnr}: {message} at {unknown_face_start_time}"
        return True, img, descriptor

    # If only one face present then proceed to identity check
    for face in faces:
        landmarks = predictor(gray, face)
        # Extract face from the camera
        x, y, width, height = face.left(), face.top(), face.width(), face.height()
        cv.rectangle(img, (x, y), (x + width, y + height), color=(0, 0, 255), thickness=5)
        face_img = img[y:y + height, x:x + width]

        if face_img.size == 0:
            continue

        face_img_rgb = cv.cvtColor(face_img, cv.COLOR_BGR2RGB)

        # Compare the face with the known faces
        face_encoding = fr.face_encodings(face_img_rgb)
        name = "Unknown"
        accuracy = 0

        if len(face_encoding) > 0:
            face_encoding = face_encoding[0]
            results = fr.compare_faces(known_face_encoding, face_encoding)

            if True in results:
                matched_index = results.index(True)
                name = known_names[matched_index]
                
                if str(matrikelnr) in name:
                    face_distances = fr.face_distance(known_face_encoding, face_encoding)
                    accuracy = round((1 - face_distances[matched_index]) * 100, 2)
                else: 
                    message = "Face doesn't match matrikelnr."
                    unknown_face_start_time = time.time()
                    unknown_face_start_time = str(datetime.fromtimestamp(unknown_face_start_time))
                    descriptor = f"{matrikelnr}: {message} at {unknown_face_start_time}"
                    x, y, width, height = face.left(), face.top(), face.width(), face.height()
                    cv.rectangle(img, (x, y), (x + width, y + height), color=(0, 0, 255), thickness=5)
                    return True, img, descriptor
                
            if name == "Unknown":
                unknown_face_start_time = time.time()
                unknown_face_start_time = str(datetime.fromtimestamp(unknown_face_start_time))

        # Draw a bounding box around the face and write the name below it
        cv.putText(img, f"{name} ({accuracy}%)", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Draw landmarks on the face
        for n in range(81):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv.circle(img, (x, y), 2, (0, 255, 0), -1)

    # Print messages
    if unknown_face_start_time is not None:
        message = "Unknown face"
        print(message)
        descriptor = f"{matrikelnr}: {message} at {unknown_face_start_time}"
        return True, img, descriptor

    return False, img, None


