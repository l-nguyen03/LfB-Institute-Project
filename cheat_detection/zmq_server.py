import zmq
import base64
import os
from datetime import datetime

# Create a ZMQ context
context = zmq.Context()

# Create a ZMQ socket for receiving text data
socket_f = context.socket(zmq.SUB)

# Subscribe to all messages from the server
socket_f.setsockopt_string(zmq.SUBSCRIBE, "")

# Connect the socket to the server
socket_f.connect("tcp://localhost:5555")

# Create a second ZMQ socket for receiving image data
socket_fe = context.socket(zmq.SUB)

# Subscribe to all messages from the second server
socket_fe.setsockopt_string(zmq.SUBSCRIBE, "")

# Connect the second socket to the server
socket_fe.connect("tcp://localhost:5556")

# Create a ZMQ socket for receiving text data
socket_a = context.socket(zmq.SUB)

# Subscribe to all messages from the server
socket_a.setsockopt_string(zmq.SUBSCRIBE, "")

# Connect the socket to the server
socket_a.connect("tcp://localhost:5557")

# Create a second ZMQ socket for receiving image data
socket_ae = context.socket(zmq.SUB)

# Subscribe to all messages from the second server
socket_ae.setsockopt_string(zmq.SUBSCRIBE, "")

# Connect the second socket to the server
socket_ae.connect("tcp://localhost:5558")

# Create the frame_evidence_zmq directory if it does not exist
if not os.path.exists('frame_evidence_zmq'):
    os.makedirs('frame_evidence_zmq')

# Create the audio_evidence_zmq directory if it does not exist
if not os.path.exists('audio_evidence_zmq'):
    os.makedirs('audio_evidence_zmq')

# Receive messages in a loop
while True:
    # Receive text messages
    message_f = socket_f.recv_string()
    print("Received message: " + message_f)
    message_a = socket_a.recv_string()
    print("Received message: " + message_a)

    # Receive image data
    image_data = socket_fe.recv_string()
    image_data = base64.b64decode(image_data)

    # Receive audio data
    audio_data = socket_ae.recv_string()
    audio_data = base64.b64decode(audio_data)

    # Save the image
    with open(os.path.join('frame_evidence_zmq', f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}.jpg'), 'wb') as image_file:
        image_file.write(image_data)

    # Save the audio evidence
    evidence_num = 1
    filename = f"audio_evidence_{evidence_num}.mp3"
    filepath = os.path.join('audio_evidence_zmq', filename)
    while os.path.exists(filepath):
        evidence_num += 1
        filename = f"audio_evidence_{evidence_num}.mp3"
        filepath = os.path.join('audio_evidence_zmq', filename)
    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio_data)
