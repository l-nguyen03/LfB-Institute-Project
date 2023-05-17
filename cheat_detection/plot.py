import pandas as pd
import matplotlib.pyplot as plt
import os 
import librosa
import librosa.display
import random
import numpy as np

script_path = os.path.abspath(__file__)
dirname = os.path.dirname(script_path)
log_dir = os.path.join(dirname, "logs")

"""
Plot learning curves for a given csv file 
and save the image in a directory called plot

<Argument> : <Argument Type>
filepath :(string) path to csv file
title : (string) title of the plot
"""
def plot_learning_curve(filepath, title = None):
    df = pd.read_csv(filepath)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df["epoch"], df["loss"], label="Training Loss", color= "blue", linestyle="-")
    ax1.plot(df["epoch"], df["val_loss"], label="Validation Loss", color="orange", linestyle="--")
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Loss", color="purple")
    ax1.tick_params(axis="y", labelcolor="purple")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(df["epoch"], df["accuracy"], label="Training Accuracy", color="blue", linestyle="-")
    ax2.plot(df["epoch"], df["val_accuracy"], label="Validation Accuracy", color="orange", linestyle="--")
    ax2.set_ylabel("Accuracy", color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.legend(loc="upper right")

    #Save the plot as a PNG file
    if title is not None:
        output_file = os.path.join(dirname, "plot", title)
        plt.title(title.replace("_", " ").replace(".png", "").title())
        plt.savefig(output_file)
        plt.show()
    else: 
        output_file = os.path.join(dirname, "plot", "leaning_curve.png")
        plt.title("Learning Curve")
        plt.savefig(output_file)
        plt.show()



"""
plot audio signal in waveform in a directory
<Argument> : <Argument Type>
wav_dir :(string) path to source directory
"""
def plot_audio_signal(wav_dir):
    class_names = [subdir for subdir in os.listdir(wav_dir) if ".DS_Store" not in subdir]
    num_rows = 1
    num_cols = 5
    # Create the figure and subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 8))
    for i, class_name in enumerate(class_names):
        subdir_path = os.path.join(wav_dir, class_name)
        wav_files = [file for file in os.listdir(subdir_path) if file.endswith(".wav")]
        selected_file = random.choice(wav_files)
        selected_file_path = os.path.join(subdir_path, selected_file)
        wav, sample_rate = librosa.load(selected_file_path)
        ax = axes[i]
        ax.plot(wav)
        ax.set_title(class_name)
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitude")
    plt.tight_layout()
    output_file = os.path.join(dirname, "plot", "representative_wavesignals.png")
    plt.savefig(output_file)
    plt.show()




"""
plot audio signal in waveform in a directory
<Argument> : <Argument Type>
wav_dir :(string) path to source directory
"""
def plot_mel_spectrogram(wav_dir): 
    class_names = [subdir for subdir in os.listdir(wav_dir) if ".DS_Store" not in subdir]
    num_rows = 1
    num_cols = 5
    # Create the figure and subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 8))
    for i, class_name in enumerate(class_names):
        subdir_path = os.path.join(wav_dir, class_name)
        wav_files = [file for file in os.listdir(subdir_path) if file.endswith(".wav")]
        selected_file = random.choice(wav_files)
        selected_file_path = os.path.join(subdir_path, selected_file)
        wav, sample_rate = librosa.load(selected_file_path)
        mel_spectrogram = librosa.feature.melspectrogram(y=wav, sr=sample_rate)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

        #plot the melspectrogram
        ax = axes[i]
        ax.set_title(class_name)
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")
        ax.set_xticks([])
        ax.set_yticks([])
        librosa.display.specshow(mel_spectrogram_db, sr=sample_rate, ax=ax)
    
    plt.tight_layout()
    output_file = os.path.join(dirname, "plot", "mel_spectrogram.png")
    plt.savefig(output_file)
    plt.show()

def plot_mfcc(wav_dir):
    class_names = [subdir for subdir in os.listdir(wav_dir) if ".DS_Store" not in subdir]
    num_rows = 1
    num_cols = 5
    # Create the figure and subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 8))
    for i, class_name in enumerate(class_names):
        subdir_path = os.path.join(wav_dir, class_name)
        wav_files = [file for file in os.listdir(subdir_path) if file.endswith(".wav")]
        selected_file = random.choice(wav_files)
        selected_file_path = os.path.join(subdir_path, selected_file)
        wav, sample_rate = librosa.load(selected_file_path)
        mfccs = librosa.feature.mfcc(y=wav, sr=sample_rate, n_mfcc=20)

        #plot the mfccs
        ax = axes[i]
        ax.set_title(class_name)
        ax.set_xlabel("Time")
        ax.set_ylabel("Index of Coefficients")
        ax.set_xticks([])
        ax.set_yticks([])
        img = librosa.display.specshow(mfccs, ax=ax)
        fig.colorbar(img, ax=ax)
    
    plt.tight_layout()
    output_file = os.path.join(dirname, "plot", "mfccs.png")
    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    plot_learning_curve(os.path.join(log_dir, "train_history.csv"))
    plot_audio_signal(os.path.join(dirname, "test"))
    plot_mel_spectrogram(os.path.join(dirname, "test"))
    plot_mfcc(os.path.join(dirname, "test"))