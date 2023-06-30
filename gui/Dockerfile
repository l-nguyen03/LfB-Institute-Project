# syntax=docker/dockerfile:1
FROM ubuntu:22.04

WORKDIR /gui

# Copy required files to the container
COPY streamlit_gui_docker.py /gui/streamlit_gui_docker.py
COPY zmq_receiver_docker.py /gui/zmq_receiver_docker.py
COPY requirements.txt /gui/requirements.txt

# Install required dependencies for audio streaming
RUN apt-get update && \
    apt-get install -y \
        wget \
        portaudio19-dev \
        libsndfile1 \
        ffmpeg \
        python3-pip \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

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

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5555
EXPOSE 5556
EXPOSE 5558
EXPOSE 8501

# Set the entry point to run the scripts
ENTRYPOINT [ "/bin/bash", "-c", "streamlit run /gui/streamlit_gui_docker.py & python3 /gui/zmq_receiver_docker.py"]