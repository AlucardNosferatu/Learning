import os

import cv2
import numpy as np
import tensorflow as tf

input_shape = (512, 512)


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
    for file in files:
        if blacklist is None or without(file, blacklist):
            img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            img_array = cv2.resize(src=img_array, dsize=input_shape, interpolation=cv2.INTER_CUBIC)
            images.append(img_array)
            labels.append(label)
    return images, labels


def create_model():
    vgg16 = tf.keras.applications.VGG16(include_top=False, classes=2, input_shape=input_shape)
    vgg16.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )
    return vgg16


model = create_model()


def read_all():
    blacklist='_mask.jpg'
    benign_folder = 'Data/恶性'
    images_, labels_ = read_folder(folder=benign_folder, label=0, n_classes=2)
    malignant_folder = 'Data/良性'
    images_, labels_ = read_folder(folder=malignant_folder, label=1, n_classes=2, images=images_, labels=labels_)
    images_ = np.array(images_)
    labels_ = np.array(labels_)
    return images_, labels_


read_all()
