import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, GlobalAveragePooling2D
from tensorflow.keras import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from Parser import counter_loader
from Config import H_Counter, W_Counter, EP, BS_Counter, ModelPath_Counter

train_images, train_labels, mc = counter_loader()
print(train_images.shape)
print(train_labels.shape)


class MyModel(Model):
    def __init__(self, mc):
        super(MyModel, self).__init__()
        self.f1 = Flatten(input_shape=(3, 256))
        self.d1 = Dense(512, activation='relu')
        self.d2 = Dense(256, activation='relu')
        self.d3 = Dense(512, activation='relu')
        self.d4 = Dense(256, activation='relu')
        self.d5 = Dense(mc, activation='softmax')

    def call(self, x):
        x = self.f1(x)
        x = self.d1(x)
        x = self.d2(x)
        x = self.d3(x)
        x = self.d4(x)
        return self.d5(x)


class VGG16(Model):
    def __init__(self, mc):
        super(VGG16, self).__init__()
        # Block 1
        self.conv1 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1',
                            input_shape=(H_Counter, W_Counter, 3))
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')
        self.bn2 = tf.keras.layers.BatchNormalization()
        self.pool1 = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')
        # Block 2
        self.conv3 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')
        self.bn3 = tf.keras.layers.BatchNormalization()
        self.conv4 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')
        self.bn4 = tf.keras.layers.BatchNormalization()
        self.pool2 = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')
        # Block 3
        self.conv5 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')
        self.bn5 = tf.keras.layers.BatchNormalization()
        self.conv6 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')
        self.bn6 = tf.keras.layers.BatchNormalization()
        self.conv7 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')
        self.bn7 = tf.keras.layers.BatchNormalization()
        self.pool3 = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')
        # Block 4
        self.conv8 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')
        self.bn8 = tf.keras.layers.BatchNormalization()
        self.conv9 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')
        self.bn9 = tf.keras.layers.BatchNormalization()
        self.conv10 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')
        self.bn10 = tf.keras.layers.BatchNormalization()
        self.pool4 = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')
        # Block 5
        self.conv11 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')
        self.bn11 = tf.keras.layers.BatchNormalization()
        self.conv12 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')
        self.bn12 = tf.keras.layers.BatchNormalization()
        self.conv13 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')
        self.bn13 = tf.keras.layers.BatchNormalization()
        self.pool5 = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')
        # Output Block
        self.f1 = Flatten()
        self.d1 = Dense(4096, activation='relu')
        self.d2 = Dense(4096, activation='relu')
        self.d3 = Dense(32, activation='relu')
        self.d4 = Dense(mc, activation='softmax')

    def call(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.pool1(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.conv4(x)
        x = self.bn4(x)
        x = self.pool2(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.conv6(x)
        x = self.bn6(x)
        x = self.conv7(x)
        x = self.bn7(x)
        x = self.pool3(x)
        x = self.conv8(x)
        x = self.bn8(x)
        x = self.conv9(x)
        x = self.bn9(x)
        x = self.conv10(x)
        x = self.bn10(x)
        x = self.pool4(x)
        x = self.conv11(x)
        x = self.bn11(x)
        x = self.conv12(x)
        x = self.bn12(x)
        x = self.conv13(x)
        x = self.bn13(x)
        x = self.pool5(x)
        x = self.f1(x)
        x = self.d1(x)
        x = self.d2(x)
        return self.d4(x)


def ResNetReg(mc, final_layer_of_resnet=176):
    res_net = tf.keras.applications.ResNet50(weights='imagenet', include_top=True)
    for layers in res_net.layers[:final_layer_of_resnet]:
        layers.trainable = False
    X = res_net.layers[final_layer_of_resnet].output
    predictions = Dense(mc, activation='softmax')(X)
    model = Model(inputs=res_net.input, outputs=predictions)
    return model


def SeqCustomModel(mc):
    model = tf.keras.Sequential(
        [
            Flatten(input_shape=(3, 256)),
            Dense(512, activation='relu'),
            Dense(256, activation='relu'),
            Dense(512, activation='relu'),
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(mc, activation='softmax')
        ]
    )
    model.compile(
        tf.keras.optimizers.Adam(0.0001),
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
        metrics=['accuracy']
    )
    return model


if (os.path.exists(ModelPath_Counter)):
    model = tf.keras.models.load_model(ModelPath_Counter)
else:
    model = SeqCustomModel(mc)

cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=ModelPath_Counter,
    save_weights_only=False,
    verbose=1
)

with tf.device('/gpu:0'):
    model.fit(
        train_images,
        train_labels,
        epochs=EP,
        batch_size=BS_Counter,
        callbacks=[cp_callback]
    )
