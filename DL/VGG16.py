# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 22:02:56 2017

@author: Scrooge
"""

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt

img_path = 'psb.jpg'
img = image.load_img(img_path, target_size=(224, 224))
plt.imshow(img)
plt.show()

model = VGG16(include_top=True, weights='imagenet')
print(type(model))

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
print(x.max())
scores = model.predict(x)

class_table = open('./data/synset_words', 'r')
lines = class_table.readlines()
print("scores type: ", type(scores))
print("scores shape: ", scores.shape)
print(np.argmax(scores))
print('result is ', lines[np.argmax(scores)])
class_table.close()

del model

model = VGG16(weights='imagenet', include_top=False)
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
features = model.predict(x)

print(features.shape)

model_extractfeatures = Model(input=model.input, output=model.get_layer('block5_pool').output)
block5_pool_features = model_extractfeatures.predict(x)
print(type(block5_pool_features))
print(block5_pool_features.shape)
feature_image = block5_pool_features[:,:,:,0].reshape(7,7)
plt.imshow(feature_image)
plt.show()