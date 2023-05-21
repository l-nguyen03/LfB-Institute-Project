import os 
from sklearn.preprocessing import LabelEncoder
from scipy.io import wavfile
import random
import numpy as np
import json

script_path = os.path.abspath(__file__)
dirname = os.path.dirname(script_path)

"""
get all the wavfile's path in a given directory 

<Argument> : <Argument Type>
src_dir: string

<Return Var> : <Return Type>
wav_paths : list of wavefile's paths.
"""
def get_wav(src_dir):
    wav_paths = []

    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(".wav"):
                wav_path = os.path.join(dirpath, filename)
                wav_paths.append(wav_path)
    return wav_paths


"""
Return the corresponding labels of all wavefiles in a given directory
Create a label encoding from categorical to integer, save this encoding as
a json file.

<Argument> : <Argument Type>
src_dir : string
wav_paths: list of wavefile's path in src_dir

<Return Var> : <Return Type>
num_classes : int
labels : list of corresponding labels.
"""
def get_labels(src_dir, wav_paths=None):      
    classes = [class_name.replace("_cleaned", "") for class_name in os.listdir(src_dir) 
           if ".DS_Store" not in class_name]
    classes.sort()
    num_classes = len(classes)
    label_encoder = LabelEncoder()
    label_encoder.fit(classes)
    if "json_mapping.json" not in os.listdir(dirname):
            label_mapping = {label: index for index, label in enumerate(label_encoder.classes_)}
            with open("json_mapping.json", "w") as f:
                json.dump(label_mapping, f)
    if wav_paths is not None:
        labels = [os.path.split(path)[0].split(os.path.sep)[-1] for path in wav_paths]
        labels = label_encoder.transform(labels)
        return [num_classes, labels]



"""
Perform arbitrary time-shifting to the left and right of all wavefiles in a 
given directory using the shift_range and save it in the same directory. 
This is useful when dataset is small.

<Argument> : <Argument Type>
src_dir : (string) path to directory
shift_range : (float) number of seconds to shift the data

<Return Var> : <Return Type>
None
"""
def shift_wav(src_dir, shift_range):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(".wav"):
                path = os.path.join(dirpath, filename)
                rate, wav = wavfile.read(path)
                max_shift_samples = int(shift_range * rate)
                for i in range(1,3):
                    shift_samples = random.randint(-max_shift_samples, max_shift_samples)
                    shifted_wav = np.roll(wav, shift_samples)
                    filename = filename.replace(".wav", "")
                    output_path = os.path.join(dirpath, f"{filename}_shifted_{i}.wav" )
                    wavfile.write(output_path, rate, shifted_wav)


if __name__ == "__main__":
    """
    #src_dir = "/Users/nptlinh/Desktop/LfB-Institute-Project/cheat_detection/dataset/Working"
    shift_wav(src_dir, 1)
    """