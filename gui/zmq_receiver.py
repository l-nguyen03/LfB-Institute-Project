import zmq
import cv2 as cv
import numpy as np
import os
from scipy.io import wavfile
from datetime import datetime
import threading
import queue

SAMPLE_RATE = 16000

dir_path = os.path.dirname(os.path.abspath(__file__))
evidence_dir = os.path.join(dir_path, "evidence")
os.makedirs(evidence_dir, exist_ok=True)

context = zmq.Context()

# Initiate Socket for image frames
socket_frame = context.socket(zmq.SUB)
socket_frame.bind("tcp://*:5555")
socket_frame.setsockopt_string(zmq.SUBSCRIBE, "frame_evidence")

# Inititate Socket for audio data
socket_audio = context.socket(zmq.SUB)
socket_audio.bind("tcp://*:5556")
socket_audio.setsockopt_string(zmq.SUBSCRIBE, "audio_evidence")



"""
This function reads receiving frames sent via ZeroMQ,
converts the frame bytes into frames and saves it in a folder named
frame_evidence. It will continually run until stop_event is set
"""
def receive_frame(stop_event):
    while not stop_event.is_set():
        if socket_frame.poll(1): # Check if there's a message on the image frame socket
            _, frame_bytes, descriptor_bytes = socket_frame.recv_multipart()

            descriptor = descriptor_bytes.decode()
            print(f"Frame description: {descriptor}")

            behaviour = descriptor.split(" at ")[0]
            frame = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame_decoded = cv.imdecode(frame, cv.IMREAD_COLOR)

            date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            image_path = os.path.join(evidence_dir, f"{behaviour}_{date_time}.jpg")
            cv.imwrite(image_path, frame_decoded)



"""
This function reads receiving audio sent via ZeroMQ,
converts the audio bytes into frames and saves it in a folder named
audio_evidence. It will continually run until stop_event is set
"""
def receive_audio(stop_event):
    while not stop_event.is_set():
        if socket_audio.poll(1): # Check if there's a message on the audio data socket
            _, audio_bytes, descriptor_bytes = socket_audio.recv_multipart()

            descriptor = descriptor_bytes.decode()
            print(f"Audio description: {descriptor}")

            # Convert the bytes back to original audio data format
            audio_data = np.frombuffer(audio_bytes, dtype=np.int16).transpose()

            behaviour = descriptor.split(" ")[0]
            date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            audio_path = os.path.join(evidence_dir, f"{behaviour}_{date_time}.wav")
            wavfile.write(audio_path, SAMPLE_RATE, audio_data)



if __name__ == "__main__":
    stop_event = threading.Event()

    # Create threads for each function
    thread_frame = threading.Thread(target=receive_frame, args=(stop_event,))
    thread_audio = threading.Thread(target=receive_audio, args=(stop_event,))
    try:
        # Start the threads
        thread_frame.start()
        thread_audio.start()
        # Wait for both threads to complete
        thread_frame.join()
        thread_audio.join()
    except KeyboardInterrupt:
        stop_event.set()
        socket_audio.close()
        socket_frame.close()
        context.term()

