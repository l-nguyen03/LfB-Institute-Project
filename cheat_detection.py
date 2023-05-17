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
Record the microphone's input every 2.5 seconds, save it as a wavfile and 
pass this file to the CNN using predict_audio for prediction. When CNN predicts the audio 
as cheating behaviour, it will print to the console and save this audio for evidence in a 
directory called audio_evidence.

<Argument Name>: <Argument Type>
None
<Return Variable>: <Return Type>
None
'''
def audio_detection(num_chunks):
    stream.start_stream()
    #start recording
    data = stream.read(CHUNK*num_chunks)
    stream.stop_stream()
    recorded_audio = np.frombuffer(data, dtype=np.int16)
    predict_audio(recorded_audio, SAMPLE_RATE)

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
    if not cap.isOpened():
        print("Error opening video capture")

    else:
        threading.Thread(target=face_monitor_thread, args=(stop_event,)).start()
        #Loop unitl interrupt with Ctrl+C
        while True:
            try:
                audio_detection(num_chunks)
            except KeyboardInterrupt:
                stop_event.set()
                stream.close()
                audio.terminate()
                break

cap.release()
cv.destroyAllWindows()