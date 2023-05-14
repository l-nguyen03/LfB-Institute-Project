import numpy as np
import cv2 as cv
from faceRecognition import camera_monitor


'''
The function captures a frame using OpenCV and pass
the frame to another function to detect whether the student 
cheats or not. If the student cheats, the captured 

<Argument Name>: <Argument Type>
void

<Return Variable>: <Return Type>
void
'''
def face_monitor():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening video capture")
        return
    
    ret, frame = cap.read()
    cheat = camera_monitor(frame)
    if cheat: 
        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        out = cv.VideoWriter('output.avi', fourcc, 20.0, frame.shape[:2][::-1])

        # Vertically flip the frame
        frame = cv.flip(frame, 1)

        # Write the flipped frame
        out.write(frame)
        out.release()

    cap.release()
    cv.destroyAllWindows()


'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def face_counter():
    pass



'''
Describe concisely about what the function does and specify: 

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def audio_detection():
    pass


'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def prepare_message():
    pass


if __name__ == "__main__":

    while True:
        try:
            face_monitor()
            
        except KeyboardInterrupt:
            break

