import numpy as np
import cv2 as cv
from faceRecognition import camera_monitor
import time
import os
import threading

dir_path = os.path.dirname(os.path.abspath(__file__))

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
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame!")
    else:
        cheat, frame, date_time = camera_monitor(frame)
        if cheat: 
            cv.imwrite(os.path.join(dir_path, "frame_evidence", f"{date_time}.jpg"), frame)



'''
This function defines a thread that calls face_monitor every 30 seconds
until stop_event is set. 
'''
def face_monitor_thread(stop_event):
    while not stop_event.is_set():
        face_monitor()
        stop_event.wait(5)



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
    stop_event = threading.Event()
    cap = cv.VideoCapture(0)
    time.sleep(2)
    if not cap.isOpened():
        print("Error opening video capture")
    else:
        threading.Thread(target=face_monitor_thread, args=(stop_event,)).start()
        while True: 
            try:
                audio_detection()
            except KeyboardInterrupt:
                stop_event.set()
                break 
    
    cap.release()
    cv.destroyAllWindows()