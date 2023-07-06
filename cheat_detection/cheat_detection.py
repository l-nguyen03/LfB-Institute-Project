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
import pdb


dir_path = os.path.dirname(os.path.abspath(__file__))

SAMPLE_RATE = 16000
DURATION = 3
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1


'''
The function captures a frame using OpenCV and pass
the frame to another function to detect whether the student 
cheats or not. If the student cheats, the captured frame 
and a brief description containing the behaviour and timestamp
will be returned. The function then sends this frame and description
to a GUI via ZeroMQ

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
        cheat, frame, descriptor = camera_monitor(frame, TEST_TAKER)
        if cheat:
            #image_path = os.path.join(dir_path, "frame_evidence", f"{date_time}.jpg")
            _, frame_encoded = cv.imencode('.jpg', frame)
            frame_bytes = frame_encoded.tobytes()
            topic = "frame_evidence"
            socket_frame.send_multipart([topic.encode(), frame_bytes, descriptor.encode()])



'''
This function defines a thread that calls face_monitor every 30 seconds
until stop_event is set. 
'''
def face_monitor_thread(stop_event):
    while not stop_event.is_set():
        face_monitor()
        stop_event.wait(5)

'''
Process the audio stored in audio_queue by passing the
recorded audio to a function that uses CNN to predict. The function
will return the audio and a brief description if cheating is 
detected. This function then sends this audio and description via ZeroMQ.
This functions runs until stop_event is set
'''
def audio_detection(stop_event, audio_queue):
    while not stop_event.is_set():
        if not audio_queue.empty():
            recorded_audio = audio_queue.get()
            cheat, descriptor, audio =  predict_audio(recorded_audio, SAMPLE_RATE, TEST_TAKER)
            if cheat: 
                audio_bytes = audio.tobytes()
                topic = "audio_evidence"
                socket_audio.send_multipart([topic.encode(), audio_bytes, descriptor.encode()])


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
This function listens to the proctor's socket to see if any command is given
If the command is to disqualify the student, the program will terminate

'''
def receive_proctor_message():
    if socket_proctor.poll(1):
        # Check if there's a message on the image frame socket
        _, descriptor_bytes = socket_proctor.recv_multipart()

        descriptor = descriptor_bytes.decode()
        print(descriptor)
        raise Exception("Disqualified")



if __name__ == "__main__":
    while True:
        try:
            TEST_TAKER = int(input("Please input your Matrikelnr.: "))
        except ValueError:
            print("Please only insert number")
            continue
        break
    
    try:
        context = zmq.Context()
        
        #Initiate socket for sending image frame
        socket_frame = context.socket(zmq.PUB)
        socket_frame.connect("tcp://localhost:5555")

        #Initiate socket for sending audio frame
        socket_audio = context.socket(zmq.PUB)
        socket_audio.connect("tcp://localhost:5556")

        #Initiate socket for receiving proctor's commmand
        socket_proctor = context.socket(zmq.SUB)
        socket_proctor.connect("tcp://localhost:5558")
        socket_proctor.setsockopt_string(zmq.SUBSCRIBE, f"{TEST_TAKER}_DISQUALIFIED")

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
            thread1 = threading.Thread(target=face_monitor_thread, args=(stop_event,))
            thread1.daemon = True
            thread2 = threading.Thread(target=audio_recording, args=(stop_event, num_chunks))
            thread2.daemon = True
            thread3 = threading.Thread(target=audio_detection, args=(stop_event, audio_queue))
            thread3.daemon = True
            thread1.start()
            thread2.start()
            thread3.start()
            #Loop unitl interrupt with Ctrl+C
            while True:
                receive_proctor_message()
    except KeyboardInterrupt:
        print("Program terminated by user.....")
    except Exception as e:
        print(e)
    finally:
        # In case of exception or manual termination, ensure all resources are properly cleaned up
        stop_event.set()
        #Check whether audio stream still running.
        if 'stream' in locals():
            stream.close()
        if 'audio' in locals():
            audio.terminate()
        socket_audio.close()
        socket_frame.close()
        socket_proctor.close()
        context.term()
        cap.release()
        cv.destroyAllWindows()