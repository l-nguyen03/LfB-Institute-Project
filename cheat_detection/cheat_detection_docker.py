import av
import cv2 as cv
import numpy as np
import time
from faceRecognition import camera_monitor
import time
import os
import threading
from queue import Queue
from predict import predict_audio

SAMPLE_RATE = 16000

dir_path = os.path.dirname(os.path.abspath(__file__))

'''
The function captures a frame using OpenCV and pass
the frame to another function to detect whether the student 
cheats or not. If the student cheats, the captured frame is 
save in a directory called frame_evidence

<Argument Name>: <Argument Type>
void

<Return Variable>: <Return Type>
void

'''
def face_monitor(stop_event, video_queue):
    while not stop_event.is_set():
        if not video_queue.empty():
            frame = video_queue.get()
            cheat, frame, date_time = camera_monitor(frame)
            if cheat:
                cv.imwrite(os.path.join(dir_path, "frame_evidence", f"{date_time}.jpg"), frame)

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
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def prepare_message():
    pass



def read_video_stream(stop_event, video_queue):
    # Open the UDP video stream
    video_container = av.open('udp://host.docker.internal:12345', 'r')
    # Loop through the video frames in the stream
    for frame in video_container.decode():
        if isinstance(frame, av.VideoFrame):
            bgr_frame = frame.reformat(format="bgr24")
            # Create an empty numpy array of the same shape as the frame
            video_frame = np.empty_like(bgr_frame.to_ndarray())
            # Convert the frame to BGR24 numpy array
            cv.cvtColor(bgr_frame.to_ndarray(), cv.COLOR_BGR2RGB, dst=video_frame)
            video_queue.put(video_frame)

        # Check if stop_event is set, then break the loop
        if stop_event.is_set():
            break



def read_audio_stream(stop_event, audio_queue):
    # Open the UDP audio stream
    audio_container = av.open('udp://host.docker.internal:12346', 'r')

    # Temporary audio buffer and its total sample count
    audio_buffer = []
    buffer_samples = 0

    # Desired chunk size (in samples)
    chunk_samples = 16000 * 2.5

    # Loop through the audio frames in the stream
    for frame in audio_container.decode():
        if isinstance(frame, av.AudioFrame):
            audio_frame = frame.to_ndarray().astype(np.float32)
            # Scale the float audio data to 16-bit integer range
            audio_frame = (audio_frame * 32767).astype(np.int16)

            # Append the audio frame to the buffer
            audio_buffer.append(audio_frame)
            buffer_samples += audio_frame.shape[0]

            # If the total number of samples in the buffer is greater than or equal to the desired chunk size,
            # put the buffer into the queue and clear it
            if buffer_samples >= chunk_samples:
                audio_queue.put(np.concatenate(audio_buffer))
                audio_buffer = []
                buffer_samples = 0

        # Check if stop_event is set, then break the loop
        if stop_event.is_set():
            break

if __name__ == "__main__":
    try:
        # Create the queues
        audio_queue = Queue()
        video_queue = Queue()
        stop_event = threading.Event()

        # Start the face monitor and audio detection threads
        read_video_thread = threading.Thread(target=read_video_stream, args=(stop_event, video_queue,))
        read_audio_thread = threading.Thread(target=read_audio_stream, args=(stop_event, audio_queue,))
        face_monitor_thread = threading.Thread(target=face_monitor, args=(stop_event, video_queue,))
        audio_detection_thread = threading.Thread(target=audio_detection, args=(stop_event, audio_queue,))
        read_video_thread.start()
        read_audio_thread.start()
        face_monitor_thread.start()
        audio_detection_thread.start()

    except KeyboardInterrupt:
        stop_event.set()
        # Wait for the threads to finish
        read_video_thread.join()
        read_audio_thread.join()
        face_monitor_thread.join()
        audio_detection_thread.join()

