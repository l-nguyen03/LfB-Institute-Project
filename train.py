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
log_dir = os.path.join(dirname, "logs")

sample_rate = 16000
duration = 2.5
batch_size = 32

wav_paths = get_wav(train_dir)
class_labels = get_labels(train_dir, wav_paths)
labels = class_labels[1]
num_classes = class_labels[0]


#Split training data into train and validation set with ratio 80/20
data_train, data_val, train_label, val_label = train_test_split(wav_paths,
                                                                  labels,
                                                                  test_size=0.2,
                                                                  random_state=13)


#Stop fitting when val_loss isn't improved after 10 epochs
early_stoppping = tf.keras.callbacks.EarlyStopping(monitor = "val_loss", patience=10, verbose=1, mode="min")

"""
#5 Folds Cross Validation

kfold = KFold(n_splits=5, shuffle=True, random_state=13)

for fold, (train_indices, val_indices) in enumerate(kfold.split(data_train, train_label)):
    wav_train = [data_train[i] for i in train_indices]
    label_train = [train_label[i] for i in train_indices]
    wav_val = [data_train[i] for i in val_indices]
    label_val = [train_label[i] for i in val_indices]
    tg = DataGenerator(wav_train, label_train, sample_rate, duration, num_classes, batch_size=batch_size)
    vg = DataGenerator(wav_val, label_val, sample_rate, duration, num_classes)
    csv_path = f"{log_dir}/cross_val_fold_{fold}_history.csv"
    model = Conv2D(num_classes, sample_rate, duration)
    csv_logger = tf.keras.callbacks.CSVLogger(csv_path, append=False)
    model.fit(tg, validation_data=vg, epochs=70, verbose=1, callbacks=[early_stoppping, csv_logger])
"""

#train model and save the best performing one. 
train_data = DataGenerator(data_train,train_label, sample_rate, duration, num_classes, batch_size=batch_size)
val_data = DataGenerator(data_val, val_label, sample_rate, duration, num_classes, batch_size=batch_size)

#Callback to log training history. 
csv_path = f"{log_dir}/train_history.csv"
csv_logger = tf.keras.callbacks.CSVLogger(csv_path, append=True)

model = Conv2D(num_classes, sample_rate, duration)

#Callback to save best performing weights.
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(f"model/audio_prediction.h5", monitor="val_loss", save_best_only=True, 
                                                      save_weights_only=False, mode="auto", save_freq="epoch", verbose=1)
model.fit(train_data, validation_data=val_data, epochs=100, verbose=1, callbacks=[early_stoppping, csv_logger, model_checkpoint])
