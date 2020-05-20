import os
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Add, UpSampling2D, Flatten
from RPN_Loss import ROILoss
from Config import H, W, EP, BS_Tailor, CheckLoss
from Parser import tailor_loader
import random

PredictMode = False
train_images, train_labels = tailor_loader(NoPatch=False)
print(train_images.shape)
print(train_labels.shape)

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
print(gpus)
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(16, 3, padding='same', activation='relu', input_shape=(H, W, 3))
        self.conv2 = Conv2D(32, 3, padding='same', activation='relu')
        self.conv3 = Conv2D(64, 3, padding='same', activation='relu')
        self.pool1 = MaxPooling2D()
        self.pool2 = MaxPooling2D()
        self.pool3 = MaxPooling2D()
        self.drop1 = Dropout(0.2)
        self.drop2 = Dropout(0.2)
        self.f1 = Flatten()
        self.d1 = Dense(512, activation='relu')
        self.d2 = Dense(4)

    def call(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        # x = self.drop1(x)
        x = self.conv3(x)
        x = self.pool3(x)
        # x = self.drop2(x)
        x = self.f1(x)
        x = self.d1(x)
        return self.d2(x)


class FPN(Model):
    def __init__(self):
        super(FPN, self).__init__()
        self.conv1 = Conv2D(256, (1, 1), name='fpn_c5p5')
        self.us1 = UpSampling2D(size=(2, 2), name="fpn_p5upsampled")
        self.conv2 = Conv2D(256, (1, 1), name='fpn_c4p4')
        self.add1 = Add(name="fpn_p4add")
        self.us2 = UpSampling2D(size=(2, 2), name="fpn_p4upsampled")
        self.conv3 = Conv2D(256, (1, 1), name='fpn_c3p3')
        self.add2 = Add(name="fpn_p3add")
        # Attach 3x3 conv to all P layers to get the final feature maps.
        self.conv6 = Conv2D(256, (3, 3), padding="SAME", name="fpn_p3")
        self.conv7 = Conv2D(256, (3, 3), padding="SAME", name="fpn_p4")
        self.conv8 = Conv2D(256, (3, 3), padding="SAME", name="fpn_p5")

    def call(self, x):
        x3 = x[0]
        x4 = x[1]
        x5 = x[2]
        p5 = self.conv1(x5)
        p4 = self.add1(
            [
                self.us1(p5),
                self.conv2(x4)
            ]
        )
        p3 = self.add2(
            [
                self.us2(p4),
                self.conv3(x3)
            ]
        )
        p3 = self.conv6(p3)
        p4 = self.conv7(p4)
        p5 = self.conv8(p5)
        return [p3, p4, p5]


if os.path.exists("TrainedModels\\VGG16_COORDINATE.h5py"):
    model = tf.keras.models.load_model("TrainedModels\\VGG16_COORDINATE.h5py", custom_objects={'ROILoss': ROILoss})
else:
    vgg16 = tf.keras.applications.VGG16(weights='imagenet', include_top=True)
    for layer in vgg16.layers:
        layer.trainable = False
    fpn = FPN()
    v16_layer_indices = [10, 14, 18]
    fpn_input = []
    for i in range(0, len(v16_layer_indices)):
        fpn_input.append(vgg16.layers[v16_layer_indices[i]].output)
    FM_result = fpn(fpn_input)
    ROI_result = []
    for i in range(0, len(FM_result)):
        # p3 p4 p5
        X = Flatten(name='flat_afterFM_' + str(i))(FM_result[i])
        X = Dense(64, activation='relu')(X)
        X = Dense(4)(X)
        ROI_result.append(X)
    X = Add()(ROI_result)
    model = Model(inputs=vgg16.input, outputs=X)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.0001),
        loss=ROILoss,
        metrics=['accuracy']
    )

if PredictMode:
    index = 0
    while index < len(train_images):
        image = train_images[index]
        result = model.predict(image.reshape((1, 224, 224, 3)))
        print(result)
        r_list = list(list(result)[0])
        x1 = int(r_list[0]*224)
        y1 = int(r_list[1]*224)
        x2 = int(r_list[2]*224)
        y2 = int(r_list[3]*224)
        image *= 255
        image = image.astype("uint8")
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1, cv2.LINE_AA)
        image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_CUBIC)
        plt.imshow(image)
        plt.show()
        plt.close()
        index += 1
else:
    checkpoint = ModelCheckpoint(
        "TrainedModels\\VGG16_COORDINATE.h5py",
        monitor='val_loss',
        verbose=1,
        save_best_only=False,
        save_weights_only=False,
        mode='auto',
        save_freq='epoch'
    )

    with tf.device('/gpu:0'):
        model.fit(
            train_images,
            train_labels,
            epochs=EP,
            batch_size=BS_Tailor,
            callbacks=[checkpoint],
            verbose=int(not CheckLoss)
        )
