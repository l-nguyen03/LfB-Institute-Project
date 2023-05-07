import tensorflow as tf
from kapre import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
import numpy as np
import os
from data_generator import DataGenerator
from clean import get_labels, get_wav


script_path = os.path.abspath(__file__)
dirname = os.path.dirname(script_path)

#Load model
custom_objects = {
    'STFT': STFT,
    'Magnitude': Magnitude,
    'ApplyFilterbank': ApplyFilterbank,
    'MagnitudeToDecibel': MagnitudeToDecibel,
}
model_path = os.path.join(dirname, "model", "audio_prediction.h5")
audio_prediction = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

#Load test set
test_path = os.path.join(dirname, "test")
test_wav = get_wav(test_path)
class_labels = get_labels(test_path, test_wav)
labels = class_labels[1]
num_classes = class_labels[0]
test_wav = np.array(test_wav)
labels = np.array(labels)
test_gen = DataGenerator(test_wav, labels, 16000, 2.5, num_classes)

#Instantiate metrics
precision = tf.keras.metrics.Precision()
recall = tf.keras.metrics.Recall()
accuracy = tf.keras.metrics.Accuracy()

for index in range(len(test_gen)):
    batch_data, batch_labels = test_gen[index]
    
    # Get predictions
    predictions = audio_prediction.predict(batch_data)
    
    # Convert predictions to class labels
    predicted_labels = np.argmax(predictions, axis=-1)

    # Convert one-hot encoded labels to integer labels
    true_labels = np.argmax(batch_labels, axis=-1)

    # Update metrics
    precision.update_state(true_labels, predicted_labels)
    recall.update_state(true_labels, predicted_labels)
    accuracy.update_state(true_labels, predicted_labels)

# Get metric results
precision_result = precision.result().numpy()
recall_result = recall.result().numpy()
accuracy_result = accuracy.result().numpy()

print("Precision:", precision_result)
print("Recall:", recall_result)
print("Accuracy:", accuracy_result)










