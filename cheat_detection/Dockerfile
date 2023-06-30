# syntax=docker/dockerfile:1
FROM ubuntu:22.04

WORKDIR /cheat-detection

# Copy required files to the container
COPY requirements.txt /cheat-detection/requirements.txt
COPY cheat_detection.py /cheat-detection/cheat_detection.py
COPY faceRecognition.py /cheat-detection/faceRecognition.py
COPY json_mapping.json /cheat-detection/json_mapping.json
COPY predict.py /cheat-detection/predict.py
COPY shape_predictor_81_face_landmarks.dat /cheat-detection/shape_predictor_81_face_landmarks.dat
COPY model/ /cheat-detection/model/
COPY frame_evidence/ /cheat-detection/frame_evidence/
COPY audio_evidence/ /cheat-detection/audio_evidence/
COPY faces/ /cheat-detection/faces/

# Install required dependencies for audio streaming and PyAudio
RUN apt-get update && \
    apt-get install -y \
        wget \
        portaudio19-dev \
        libsndfile1 \
        cmake \
        build-essential \
        libopenblas-dev \
        ffmpeg \
        alsa-base \
        alsa-utils \
        pulseaudio \
        && rm -rf /var/lib/apt/lists/*

# Install Python and pip
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5555
EXPOSE 5556
EXPOSE 5558

# Set the entry point to run cheat_detection.py and read from microphone
ENTRYPOINT ["python3", "cheat_detection.py"]


