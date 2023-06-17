# syntax=docker/dockerfile:1
FROM ubuntu:22.04


WORKDIR /gui
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Copy require files to the container
COPY streamlit_gui.py /gui/streamlit_gui_docker.py
COPY zmq_receiver.py /gui/zmq_receiver_docker.py

# Install required dependencies for audio streaming
RUN apt-get update && \
    apt-get install -y \
        wget \
        portaudio19-dev \
        libsndfile1 \
        ffmpeg \
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

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

# Create a new Python 3.9 environment named "gui"
RUN conda create -y -n gui python=3.9

RUN echo "source /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate gui" >> ~/.bashrc && \
    /bin/bash -c "source /root/miniconda3/etc/profile.d/conda.sh && \
    conda activate gui && \
    pip install --no-cache-dir -r requirements.txt"

EXPOSE 5555
EXPOSE 5556
EXPOSE 5558

# Set the entry point to start a shell with the environment activated
ENTRYPOINT [ "/bin/bash", "-c", "source /root/miniconda3/etc/profile.d/conda.sh && conda activate gui && python3 /gui/streamlit_gui_docker.py & python3 /gui/zmq_receiver_docker.py"]