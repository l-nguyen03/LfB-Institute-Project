import tensorflow as tf
from kapre import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel, LogmelToMFCC
import numpy as np
import os
import json
from scipy.io import wavfile

CHEAT = ["Computer keyboard", "Speech", "Whispering"]
NON_CHEAT = ["Working", "Traffic noise, roadway noise"]

with open("json_mapping.json", "r") as f: 
    map = json.load(f)

script_path = os.path.abspath(__file__)
dirname = os.path.dirname(script_path)

#Load model
custom_objects = {
    'STFT': STFT,
    'Magnitude': Magnitude,
    'ApplyFilterbank': ApplyFilterbank,
    'MagnitudeToDecibel': MagnitudeToDecibel,
    'LogmelToMFCC' : LogmelToMFCC
}
model_path = os.path.join(dirname, "model", "audio_prediction.h5")
    
audio_prediction = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
    
"""
Predict whether the recorded audio reflect cheating

<Argument> : <Argument Type>
wav_file : (string) path to wave file.

<Return Var> : <Return Type>
_ : (Boolean) True for non-cheat and False for cheating.
"""
def predict_audio(wav, rate):

    #classify sound event
    audio, audio_batch = audio_preprocess(wav)
    prediction = audio_prediction.predict(audio_batch)
    predicted_label = np.argmax(prediction, axis=-1)
    for category, index in map.items():
        if index == predicted_label:
            if category in CHEAT:
                print(f"CHEATING DETECTED: {category}")
                evidence_num = 1
                filename = f"evidence_{evidence_num}.wav"
                filepath = os.path.join("audio_evidence", filename)
                while os.path.exists(filepath):
                    evidence_num += 1
                    filename = f"evidence_{evidence_num}.wav"
                    filepath = os.path.join("audio_evidence", filename)
                wavfile.write(filepath, rate, audio)
                return False
            else: 
                print(category)
                return True 


"""
Reshape the given wavefile to (40000,1) and add batch dimension to feed to model.predict()
Pad with zeros if data points are less then 40000

<Argument> : <Argument Type>
wav_file : (string) path to wavefile

<Return Var> : <Return Type>
rate : sampling rate of audio
wav : reshaped wavefile of dimension (40000,1)
wav_batch : reshaped wavefile with extra batch dimension (40000, 1, 0)
"""
def audio_preprocess(wav):
    #rate, wav = wavfile.read(wav_file)
    wav = wav.reshape(-1,1)
    if wav.shape[0] < 40000:
        wav = np.pad(wav, ((0, 40000-wav.shape[0]), (0,0)), mode="constant", constant_values = 0)
    elif wav.shape[0] > 40000:
        wav = wav[:40000]
    wav_batch = np.expand_dims(wav, axis=0)

    return wav, wav_batch