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
    log_dir = os.path.join(dir_path, "log")
    os.makedirs(evidence_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    return dir_path, evidence_dir, log_dir


def remove_files(dir_path, matrikelnr):
    for filename in os.listdir(dir_path):
        # If the 'matrikelnr' substring is in the file name, delete the file
        if str(matrikelnr) in filename:
            file_path = os.path.join(dir_path, filename)
            try:
                os.remove(file_path)
                print(f"File {filename} has been deleted.")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")



def send_disqualify(behaviour, file_extension, data, log_dir, matrikelnr, evidence_dir):
    if file_extension == ".jpg":
        image_path = os.path.join(log_dir, f"{matrikelnr}_{behaviour}.jpg")
        cv.imwrite(image_path, data)
    elif file_extension == ".wav":
        audio_path = os.path.join(log_dir, f"{matrikelnr}_{behaviour}.wav")
        wavfile.write(audio_path, 16000, data)

    context = zmq.Context()
    #Initiate socket for sending disqualify decision
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5558")
    time.sleep(2)
    topic = f"{matrikelnr}_DISQUALIFIED"
    message = f"You are hereby disqualified because of cheating behaviour: {behaviour}"
    socket.send_multipart([topic.encode(), message.encode()])
    remove_files(evidence_dir, matrikelnr)
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
    dir_path, evidence_dir, log_dir = get_dir_path()
    oldest_file_path = get_oldest_file(evidence_dir)
    
    st.title("Protoring Notification Window")
    st.header("Evidence will pop up below (if any)")

    if oldest_file_path is None: 
        st.text("There isn't any cheating behaviour yet.")
        time.sleep(5)
        st.experimental_rerun()
    else: 
        oldest_file_name = os.path.basename(oldest_file_path)
        file_name, file_extension = os.path.splitext(oldest_file_name)
        if file_extension == ".jpg":
            image = cv.imread(oldest_file_path)
            behavior = file_name.split("_")[1]
            matrikelnr = file_name.split("_")[0]
            os.remove(oldest_file_path)
            with st.container():
                st.divider()
                st.text(f"Matrikelnr. {matrikelnr} - Cheating detected! {behavior}")
                st.image(image, caption=behavior, channels="BGR")
                st.button("Yes!", on_click=send_disqualify, args=(behavior, file_extension, image, log_dir, matrikelnr, evidence_dir, ))
                st.button("No.")
        elif file_extension == ".wav":
            sample_rate, audio = wavfile.read(oldest_file_path)
            behavior = file_name.split("_")[1]
            matrikelnr = file_name.split("_")[0]
            os.remove(oldest_file_path)
            with st.container():
                st.divider()
                st.text(f"Matrikelnr. {matrikelnr} - Cheating detected! {behavior}")
                st.audio(audio, sample_rate=sample_rate)
                st.button("Yes!", on_click=send_disqualify, args=(behavior, file_extension, audio, log_dir, matrikelnr, evidence_dir, ))
                st.button("No.")





