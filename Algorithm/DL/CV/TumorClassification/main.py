import os

import cv2
import numpy as np
import tensorflow as tf
from tqdm import tqdm

input_shape = (512, 512, 3)


def read_folder(folder, label, n_classes, images=None, labels=None, blacklist=None):
    def without(fname, blist):
        for keyword in blist:
            if keyword in fname:
                return False
        return True

    label = np.eye(n_classes)[label, :]
    files = os.listdir(folder)
    files = [os.path.join(folder, file) for file in files]
    if images is None:
        images = []
    if labels is None:
        labels = []
    for file in tqdm(files):
        if blacklist is None or without(file, blacklist):
            img_array = cv2.imread(file, cv2.IMREAD_COLOR)
            img_array = cv2.resize(src=img_array, dsize=(input_shape[0], input_shape[1]), interpolation=cv2.INTER_CUBIC)
            images.append(img_array)
            labels.append(label)
    return images, labels


def read_all():
    blacklist = ['_mask.jpg', '.DS_Store']
    benign_folder = 'Data\\benign'
    malignant_folder = 'Data\\malignant'
    images, labels = read_folder(
        folder=benign_folder,
        label=0,
        n_classes=2,
        blacklist=blacklist
    )
    images, labels = read_folder(
        folder=malignant_folder,
        label=1,
        n_classes=2,
        images=images,
        labels=labels,
        blacklist=blacklist
    )
    images = np.array(images)
    labels = np.array(labels)
    return images, labels


def create_model(n_classes=2):
    vgg16 = tf.keras.applications.VGG16(include_top=False, input_shape=input_shape)
    for i in range(len(vgg16.layers)):
        vgg16.layers[i].trainable = False
    x = tf.keras.layers.Flatten()(vgg16.output)
    x = tf.keras.layers.Dense(1024, activation=tf.keras.activations.selu)(x)
    x = tf.keras.layers.Dense(n_classes, activation=tf.keras.activations.softmax)(x)
    vgg16 = tf.keras.Model(inputs=vgg16.inputs, outputs=x)
    return vgg16


def train_model(force_update=False):
    images_, labels_ = read_all()
    filepath = 'TumorClassification.h5'
    if os.path.exists(filepath) and not force_update:
        model = tf.keras.models.load_model(filepath)
    else:
        model = create_model()
    tf.keras.utils.plot_model(
        model=model,
        to_file='vgg16.png',
        show_shapes=True,
        expand_nested=True,
        show_layer_activations=True
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )
    ckpt = tf.keras.callbacks.ModelCheckpoint(
        filepath=filepath,
        monitor='loss',
        verbose=1,
        save_best_only=True
    )
    with tf.device('/gpu:0'):
        model.fit(x=images_, y=labels_, batch_size=8, epochs=1000, shuffle=True, callbacks=[ckpt])


if __name__ == '__main__':
    train_model()
