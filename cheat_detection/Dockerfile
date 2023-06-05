# syntax=docker/dockerfile:1
FROM ubuntu:22.04


WORKDIR /cheat-detection
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Copy requirements.txt to the container
COPY requirements.txt /cheat-detection/requirements.txt
COPY cheat_detection_docker.py /cheat-detection/cheat_detection_docker.py
COPY faceRecognition.py /cheat-detection/faceRecognition.py
COPY json_mapping.json /cheat-detection/json_mapping.json
COPY predict.py /cheat-detection/predict.py
COPY shape_predictor_81_face_landmarks.dat /cheat-detection/shape_predictor_81_face_landmarks.dat
COPY model/ /cheat-detection/model/
COPY frame_evidence/ /cheat-detection/frame_evidence/
COPY audio_evidence/ /cheat-detection/audio_evidence/
COPY faces/ /cheat-detection/faces/

# Install required dependencies for PyAudio
RUN apt-get update && \
    apt-get install -y \
        wget \
        portaudio19-dev \
        libsndfile1 \
        cmake \
        build-essential \
        libopenblas-dev \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-aarch64.sh -b \
    && rm -f Miniconda3-latest-Linux-aarch64.sh

# Create a new Python 3.9 environment named "cheat_detection"
RUN conda create -y -n cheat_detection python=3.9

RUN echo "source /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate cheat_detection" >> ~/.bashrc && \
    /bin/bash -c "source /root/miniconda3/etc/profile.d/conda.sh && \
    conda activate cheat_detection && \
    pip install --no-cache-dir -r requirements.txt"

# Set the entry point to start a shell with the environment activated
ENTRYPOINT [ "/bin/bash", "-c", "source /root/miniconda3/etc/profile.d/conda.sh && conda activate cheat_detection && /bin/bash" ]

