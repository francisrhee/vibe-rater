import sys
import os
os.environ['TF_KERAS'] = '1'
import numpy as np
import pandas as pd
from skimage.io import imread
from skimage import color
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras_radam import RAdam

# from keras.applications.imagenet_utils import decode_predictions
import efficientnet.tfkeras as enet
from efficientnet.tfkeras import center_crop_and_resize, preprocess_input

CLASSIFICATION = {
    0: "Your vibes are wack",
    1: "Not vibing",
    2: "You're alright",
    3: "We vibing",
    4: "We SUPER vibing"
}
def decode_predictions(array):
    return CLASSIFICATION[np.argmax(array, axis=1)[0]]

def getPrediction(filepath):
    print("loading model", file=sys.stderr)
    
    ## Working prediction flow
    path = "./model"
    model = tf.keras.models.load_model(path, custom_objects={'RAdam': RAdam})
    image = imread(filepath)

    if image.shape[-1] == 4:
        image = color.rgba2rgb(image)

    image_size = model.input_shape[1]
    x = center_crop_and_resize(image, image_size=image_size)
    x = preprocess_input(x)
    x = np.expand_dims(x, 0)

    print(x.shape, file=sys.stderr)

    # make prediction and decode
    y = model.predict(x)
    # TODO: decode - we currently have 1/5 classes from training, how do we get percentages/confidence?
    return decode_predictions(y)

    # print("reading image", file=sys.stderr)
    # image = load_img('uploads/'+filename, target_size=(224, 224))
    # image = img_to_array(image)
    # # image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # # image = preprocess_input(image)
    # print("predicting", file=sys.stderr)
    # yhat = model.predict(image)
    # # label = decode_predictions(yhat)
    # # label = label[0][0]
    # # print('%s (%.2f%%)' % (label[1], label[2]*100))
    # # return label[1], label[2]*100
    # return yhat

    # TODO: currently getting this error: AttributeError: '_UserObject' object has no attribute 'predict'
    # TODO: maybe it has to do with using tf rather than keras? maybe it's savedmodels? 