import dlib
import cv2 as cv
import face_recognition as fr
import numpy as np
import time

# Initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/ali/Institutsprojekt/shape_predictor_81_face_landmarks.dat")  # Path for shape_predictor

# Load the known face image and encode it
student_img = fr.load_image_file("/home/ali/Institutsprojekt/faces/student.jpg")  # Path for the known faces
student_face_encoding = fr.face_encodings(student_img)[0]

known_faces = [student_face_encoding]  # List of known face encodings
known_names = ["Student"]  # List of known names

# Initialize the camera
capture = cv.VideoCapture(0)

unknown_face_start_time = None
second_person_detected = False

while True:
    ret, img = capture.read()
    if not ret:
        break

    # Convert the image to grayscale for better face detection
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) > 1:
        second_person_detected = True

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
        face_encodings = fr.face_encodings(face_img_rgb)
        name = "Unknown"
        accuracy = 0

        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            results = fr.compare_faces(known_faces, face_encoding)

            if True in results:
                matched_index = results.index(True)
                name = known_names[matched_index]
                face_distances = fr.face_distance(known_faces, face_encoding)
                accuracy = round((1 - face_distances[matched_index]) * 100, 2)

            if name == "Unknown" and unknown_face_start_time is None:
                unknown_face_start_time = time.time()
            elif name != "Unknown":
                unknown_face_start_time = None

        # Draw a bounding box around the face and write the name below it
        cv.putText(img, f"{name} ({accuracy}%)", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Draw landmarks on the face
        for n in range(68):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv.circle(img, (x, y), 2, (0, 255, 0), -1)

    # Display the image with faces and landmarks
    cv.imshow("Camera", img)

    # Print messages
    if unknown_face_start_time is not None and time.time() - unknown_face_start_time > 5:
        print("Unknown face")
    if second_person_detected:
        print("Second person detected")
        second_person_detected = False

    # Close the program with 'q'
    if cv.waitKey(1) == ord("q"):
        break

capture.release()
cv.destroyAllWindows()
