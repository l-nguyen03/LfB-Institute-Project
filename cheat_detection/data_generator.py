import tensorflow as tf
import numpy as np
from scipy.io import wavfile


"""
Implementation of a Data Generator that randomly divide data into batches in each epoch of 
training. 
"""
class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, wav_paths, labels, sr, duration, num_classes, 
                 batch_size = 32, shuffle=True):
        self.wav_paths = wav_paths
        self.labels = labels
        self.sr = sr
        self.duration = duration
        self.num_classes = num_classes
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indices = np.arange(len(self.wav_paths))
    


    """
    Return length of a batch
    """
    def __len__(self):
        length = int(np.floor(len(self.wav_paths)/self.batch_size))
        return length

    

    """
    Create an input matrix X for each batch index.
    Create a one-hot matrix Y for the corresponding labels of X.
    """
    def __getitem__(self, idx):
        indices = self.indices[idx*self.batch_size:(idx+1)*self.batch_size]
        wav_paths = [self.wav_paths[k] for k in indices]
        labels = [self.labels[k] for k in indices]

        X = np.empty((self.batch_size, int(self.sr*self.duration), 1), dtype=np.float32)
        Y = np.empty((self.batch_size, self.num_classes), dtype=np.float32)

        for i, (path, label) in enumerate(zip(wav_paths, labels)):
            rate, wav = wavfile.read(path)
            wav = wav.reshape(-1,1)
            if wav.shape[0] < 40000:
                wav = np.pad(wav, ((0, 40000-wav.shape[0]), (0,0)), mode="constant", constant_values = 0)
            X[i,] = wav.reshape(-1, 1)
            Y[i,] = tf.keras.utils.to_categorical(label, num_classes=self.num_classes)
        return X, Y
    
    """
    after each epoch, shuffle the index of the batches
    """
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)
    

