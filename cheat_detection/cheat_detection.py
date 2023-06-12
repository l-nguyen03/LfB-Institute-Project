import pyaudio
import numpy as np
from predict import predict_audio
import time
import cv2 as cv
from faceRecognition import camera_monitor
import time
import os
import threading
from queue import Queue
import zmq
import base64

dir_path = os.path.dirname(os.path.abspath(__file__))

SAMPLE_RATE = 16000
DURATION = 3
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1


'''
The function captures a frame using OpenCV and pass
the frame to another function to detect whether the student 
cheats or not. If the student cheats, the captured 

<Argument Name>: <Argument Type>
void

<Return Variable>: <Return Type>
void

'''

def zmq_faces(socket_f):
    # Path to log.txt
    log_file_path = os.path.join('frame_evidence', 'log.txt')

    # Open log.txt
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            socket_f.send_string(last_line)

# Create zmq context
context_f = zmq.Context()

# Create zmq socket
socket_f = context_f.socket(zmq.PUB)
socket_f.bind("tcp://*:5555")

def zmq_frame_evidence(socket_fe, image_path):
    # Open the image in binary mode
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Encode the image data to base64
    image_data_base64 = base64.b64encode(image_data).decode('utf-8')

    # Send the base64 encoded image
    socket_fe.send_string(image_data_base64)

# Create zmq context
context_fe = zmq.Context()

# Create zmq socket
socket_fe = context_fe.socket(zmq.PUB)
socket_fe.bind("tcp://*:5556")



def face_monitor():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame!")
    else:
        cheat, frame, date_time = camera_monitor(frame)
        if cheat:
            image_path = os.path.join(dir_path, "frame_evidence", f"{date_time}.jpg")
            cv.imwrite(image_path, frame)
            zmq_faces(socket_f)
            zmq_frame_evidence(socket_fe, image_path)


'''
This function defines a thread that calls face_monitor every 30 seconds
until stop_event is set. 
'''
def face_monitor_thread(stop_event):
    while not stop_event.is_set():
        face_monitor()
        stop_event.wait(5)

'''
Process the audio stored in audio_queue and use the CNN to predict until 
stop_event is set
'''
def audio_detection(stop_event, audio_queue):
    while not stop_event.is_set():
        if not audio_queue.empty():
            recorded_audio = audio_queue.get()
            predict_audio(recorded_audio, SAMPLE_RATE)

'''
This function defines a thread that record the microphone's input and save it in a queue
until stop_event is set. 
'''
def audio_recording(stop_event, num_chunks):
    while not stop_event.is_set():
        stream.start_stream()
        data = stream.read(CHUNK*num_chunks, exception_on_overflow=False)
        stream.stop_stream()
        recorded_audio = np.frombuffer(data, dtype=np.int16)
        audio_queue.put(recorded_audio)
        stop_event.wait(1)

'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def prepare_message():
    pass


if __name__ == "__main__":

    audio = pyaudio.PyAudio()
    #start stream
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    num_chunks = int(SAMPLE_RATE / CHUNK * DURATION)
    stop_event = threading.Event()
    cap = cv.VideoCapture(0)
    time.sleep(2)
    audio_queue = Queue()
    if not cap.isOpened():
        print("Error opening video capture")
    else:
        threading.Thread(target=face_monitor_thread, args=(stop_event,)).start()
        threading.Thread(target=audio_recording, args=(stop_event, num_chunks)).start()
        threading.Thread(target=audio_detection, args=(stop_event, audio_queue)).start()
        #Loop unitl interrupt with Ctrl+C
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                stop_event.set()
                stream.close()
                audio.terminate()
                break

cap.release()
cv.destroyAllWindows()
