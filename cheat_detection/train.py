from data_generator import DataGenerator
from clean import get_wav, get_labels
from scipy.io import wavfile
import os
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from model import Conv2D


script_path = os.path.abspath(__file__)
dirname = os.path.dirname(script_path)
train_dir = os.path.join(dirname, "train")
val_dir = os.path.join(dirname, "val")
log_dir = os.path.join(dirname, "logs")

sample_rate = 16000
duration = 2.5
batch_size = 32

wav_paths_train = get_wav(train_dir)
class_labels_train = get_labels(train_dir, wav_paths_train)
labels_train = class_labels_train[1]
num_classes = class_labels_train[0]

wav_paths_val = get_wav(val_dir)
class_labels_val = get_labels(val_dir, wav_paths_val)
labels_val = class_labels_val[1]


#Stop fitting when val_loss isn't improved after 10 epochs
early_stoppping = tf.keras.callbacks.EarlyStopping(monitor = "val_loss", patience=10, verbose=1, mode="min")


#train model and save the best performing one. 
train_data = DataGenerator(wav_paths_train, labels_train, sample_rate, duration, num_classes, batch_size=batch_size)
val_data = DataGenerator(wav_paths_val, labels_val, sample_rate, duration, num_classes, batch_size=batch_size)

#Callback to log training history. 
csv_path = f"{log_dir}/train_history.csv"
csv_logger = tf.keras.callbacks.CSVLogger(csv_path, append=False)

model = Conv2D(num_classes, sample_rate, duration)
model.summary()
"""
#Callback to save best performing weights.
model_path = os.path.join(dirname, "model", "audio_prediction.h5")
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(model_path, monitor="val_loss", save_best_only=True, 
                                                      save_weights_only=False, mode="auto", save_freq="epoch", verbose=1)
model.fit(train_data, validation_data=val_data, epochs=100, verbose=1, callbacks=[early_stoppping, csv_logger, model_checkpoint])
"""