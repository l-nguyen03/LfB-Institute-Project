import pyaudio
import numpy as np
from scipy.io import wavfile
from predict import predict_audio

SAMPLE_RATE = 16000
DURATION = 3
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def face_comparison():
    pass



'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def face_counter():
    pass



'''
Record the microphone's input every 2.5 seconds, save it as a wavfile and 
pass this file to the CNN using predict_audio for prediction. When CNN predicts the audio 
as cheating behaviour, it will print to the console and save this audio for evidence in a 
directory called audio_evidence.

<Argument Name>: <Argument Type>
None
<Return Variable>: <Return Type>
None
'''
def audio_detection(num_chunks):
    frames = []
    #start recording
    for _ in range(num_chunks):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))
    recorded_audio = np.hstack(frames)
    wavfile.write("recorded_audio.wav", SAMPLE_RATE, recorded_audio)
    predict_audio("recorded_audio.wav")


'''
Describe concisely about what the function does and specify:

<Argument Name>: <Argument Type>

<Return Variable>: <Return Type>

'''
def prepare_message():
    pass


if __name__ == "__main__":
    audio = pyaudio.PyAudio()
    #start stream
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    num_chunks = int(SAMPLE_RATE / CHUNK * DURATION)
    #Loop unitl interrupt with Ctrl+C
    while True:
        try: 
            audio_detection(num_chunks)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            break