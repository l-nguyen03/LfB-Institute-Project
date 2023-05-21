
import pyaudio
import numpy as np
from scipy.io import wavfile
from predict import predict_audio
import time
import cv2 as cv
from faceRecognition import camera_monitor
import time
import os
import threading
from queue import Queue

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