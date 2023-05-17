import tensorflow as tf
from kapre.composed import get_melspectrogram_layer
from kapre.signal import LogmelToMFCC


def Conv2D(num_classes, sample_rate, duration):
    input_shape = (int(sample_rate*duration), 1)
    input = get_melspectrogram_layer(input_shape=input_shape,
                                 n_mels=128,
                                 pad_end=True,
                                 n_fft=512,
                                 win_length=400,
                                 hop_length=160,
                                 sample_rate=sample_rate,
                                 return_decibel=True,
                                 input_data_format='channels_last',
                                 output_data_format='channels_last')
    hidden = tf.keras.layers.LayerNormalization(axis=2, name='layer_norm_1')(input.output)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='tanh', padding='same', name='conv2d_tanh_1')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='tanh', padding='same', name='conv2d_tanh_2')(hidden)
    hidden = tf.keras.layers.MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_1')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_3')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_4')(hidden)
    hidden = tf.keras.layers.MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_2')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_5')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_6')(hidden)
    hidden = tf.keras.layers.MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_3')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_7')(hidden)
    hidden = tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_8')(hidden)
    hidden = tf.keras.layers.MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_4')(hidden)
    hidden = tf.keras.layers.Flatten(name='flatten')(hidden)
    hidden = tf.keras.layers.Dropout(rate=0.5, name='dropout_2')(hidden)
    hidden = tf.keras.layers.Dense(512, activation='relu', name='dense_1', activity_regularizer=tf.keras.regularizers.l2(0.001))(hidden)
    hidden = tf.keras.layers.Dropout(rate=0.2, name='dropout_4')(hidden)
    hidden = tf.keras.layers.Dense(256, activation='relu', name='dense_3', activity_regularizer=tf.keras.regularizers.l2(0.001))(hidden)
    hidden = tf.keras.layers.Dense(128, activation='relu', name='dense_4', activity_regularizer=tf.keras.regularizers.l2(0.001))(hidden)
    output = tf.keras.layers.Dense(num_classes, activation='softmax', name='softmax')(hidden)
    model = tf.keras.models.Model(inputs=input.input, outputs=output, name='2d_convolution')
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
