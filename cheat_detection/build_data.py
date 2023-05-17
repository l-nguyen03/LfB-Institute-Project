import os 
import random
import shutil

#get absolute filepath independent of deployment
script_path = os.path.abspath(__file__)
src_dir = os.path.dirname(script_path)
dataset_path = f"{src_dir}/dataset"
dirnames = [dirname for dirname in os.listdir(dataset_path) if ".DS_Store" not in dirname ]

#Loop through each class directory and split the data into training and test sets with a ratio of 80/20
wav_files = []
for dirname in dirnames:
    for filename in os.listdir(f"{dataset_path}/{dirname}"):
        if ".DS_Store" not in filename: 
            wav_files.append(filename)
    wav_files.sort()
    random.seed(29)
    random.shuffle(wav_files)
    train_split = int(0.65 * len(wav_files))
    val_split = int(0.8 * len(wav_files))

    train_wav = wav_files[:train_split]
    val_wav = wav_files[train_split:val_split]
    test_wav = wav_files[val_split:]
    for wav_file in train_wav:
        dist_dir = f"{src_dir}/train/{dirname}"
        os.makedirs(dist_dir, exist_ok=True)
        shutil.copy(f"{dataset_path}/{dirname}/{wav_file}", dist_dir)
    for wav_file in val_wav:
        dist_dir = f"{src_dir}/val/{dirname}"
        os.makedirs(dist_dir, exist_ok=True)
        shutil.copy(f"{dataset_path}/{dirname}/{wav_file}", dist_dir)
    for wav_file in test_wav:
        dist_dir = f"{src_dir}/test/{dirname}"
        os.makedirs(dist_dir, exist_ok=True)
        shutil.copy(f"{dataset_path}/{dirname}/{wav_file}", dist_dir)
    wav_files = []