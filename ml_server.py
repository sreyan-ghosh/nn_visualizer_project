import json
import tensorflow as tf
import numpy as np
import os, re
import string
import random

from flask import Flask, request

app = Flask(__name__)

model = tf.keras.models.load_model('model.h5')
feature_model = tf.keras.Model(
    model.inputs,
    [layer.output for layer in model.layers]
)

_, (X_test, y_test) = tf.keras.datasets.mnist.load_data()
X_test = X_test/255.0

def get_prediction():
    index = np.random.choice(X_test.shape[0])
    image = X_test[index, :, :]
    image_arr = np.reshape(image, (1, 784))
    return feature_model.predict(image_arr), image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        preds, image = get_prediction()
        final_preds = [p.tolist() for p in preds]
        return json.dumps({
            'prediction': final_preds,
            'image': image.tolist()
        })
    return 'welcome to the ml server'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
