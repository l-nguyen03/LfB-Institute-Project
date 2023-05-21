import tensorflow as tf
import librosa
from kapre import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel, LogmelToMFCC
import numpy as np
import os
import json
import soundfile as sf

CHEAT = ["Computer keyboard", "Speech", "Whispering"]
NON_CHEAT = ["Working", "Siren"]
json_mapping_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_mapping.json")
evidence_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_evidence")
if not os.path.exists(evidence_path):
    os.makedirs(evidence_path)


with open(json_mapping_path, "r") as f: 
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
    
audio_prediction = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
audio_prediction.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
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
                filepath = os.path.join(evidence_path, filename)
                while os.path.exists(filepath):
                    evidence_num += 1
                    filename = f"evidence_{evidence_num}.wav"
                    filepath = os.path.join(evidence_path, filename)
                sf.write(filepath, audio, rate, format="mp3")
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
    wav = wav.reshape(-1,1)
    if wav.shape[0] < 40000:
        wav = np.pad(wav, ((0, 40000-wav.shape[0]), (0,0)), mode="constant", constant_values = 0)
    elif wav.shape[0] > 40000:
        wav = wav[:40000]
    wav_batch = np.expand_dims(wav, axis=0)

    return wav, wav_batch