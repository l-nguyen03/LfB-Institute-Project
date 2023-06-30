import os
import streamlit as st
from scipy.io import wavfile
import cv2 as cv
import zmq
import time


@st.cache_data
def get_dir_path():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    evidence_dir = os.path.join(dir_path, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    return dir_path, evidence_dir



def send_disqualify(behaviour):
    context = zmq.Context()
    #Initiate socket for sending disqualify decision
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5558")
    time.sleep(2)
    topic = "DISQUALIFIED"
    message = f"You are hereby disqualified because of cheating behaviour: {behaviour}"
    socket.send_multipart([topic.encode(), message.encode()])
    socket.close()
    context.term()



def get_oldest_file(dir_path):
    # Get list of all files in dir_path
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if 
             os.path.isfile(os.path.join(dir_path, f)) and f != ".DS_Store"]

    if not files:
        return None  # No files to process

    # Find the oldest file
    oldest_file = min(files, key=os.path.getctime)

    return oldest_file



if __name__ == "__main__":
    dir_path, evidence_dir = get_dir_path()
    oldest_file_path = get_oldest_file(evidence_dir)
    
    st.title("Protoring Notification Window")
    st.header("Evidence will pop up below (if any)")

    if oldest_file_path is None: 
        st.text("There isn't any cheating behaviour yet.")
        st.experimental_rerun()
    else: 
        oldest_file_name = os.path.basename(oldest_file_path)
        file_name, file_extension = os.path.splitext(oldest_file_name)
        if file_extension == ".jpg":
            image = cv.imread(oldest_file_path)
            behavior = file_name.split("_")[0]
            os.remove(oldest_file_path)
            with st.container():
                st.divider()
                st.text(f"Cheating detected! {behavior}")
                st.image(image, caption=behavior, channels="BGR")
                st.button("Yes!", on_click=send_disqualify, args=(behavior,))
                st.button("No.")
        elif file_extension == ".wav":
            sample_rate, audio = wavfile.read(oldest_file_path)
            behavior = file_name.split("_")[0]
            os.remove(oldest_file_path)
            with st.container():
                st.divider()
                st.text(f"Cheating detected! {behavior}")
                st.audio(audio, sample_rate=sample_rate)
                st.button("Yes!", on_click=send_disqualify, args=(behavior,))
                st.button("No.")





