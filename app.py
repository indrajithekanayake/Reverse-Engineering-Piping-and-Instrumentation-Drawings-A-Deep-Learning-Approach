import os.path
import urllib
import uuid
import base64
import requests
import json
from urllib import request

import numpy as np
from flask import Flask, render_template, send_from_directory, request, jsonify
from keras.utils import load_img, img_to_array
from tensorflow.python.ops.image_ops_impl import rgb_to_grayscale
from werkzeug.utils import secure_filename
from keras.models import Sequential, load_model
from keras.models import Sequential, model_from_json

from PIL import Image

app = Flask(__name__)
app.config['STATIC'] = 'static'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Prediction Labels
ARRAY_OF_LABELS = ['Arrowhead', 'Arrowhead + Triangle', 'Box', 'Continuity Label',
                   'Control', 'Control Valve Globe', 'DB&BBV', 'DB&BBV + Valve Check',
                   'DB&BPV', 'ESDV Valve Ball', 'ESDV Valve Butterfly',
                   'ESDV Valve Slab Gate', 'Exit to Atmosphere', 'Flange + Triangle',
                   'Flange Joint', 'Flange Single T-Shape', 'Injector Point',
                   'Reducer', 'Rupture Disc', 'Sensor', 'Spectacle Blind', 'Triangle',
                   'Valve', 'Valve Angle', 'Valve Ball', 'Valve Butterfly',
                   'Valve Check', 'Valve Globe', 'Valve Plug', 'Valve Slab Gate'
                   ]

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# Function to perform ocr on image and convert it to pdf


def convert_image_to_pdf(image_path, API_KEY):
    instructions = {
        'parts': [
            {
                'file': 'page1.jpg'
            }
        ],
        'actions': [
            {
                'type': 'ocr',
                'language': 'english'
            }
        ]
    }

    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': 'Bearer ' + API_KEY,
        },
        files={
            'page1.jpg': open(image_path, 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )

    if response.ok:
        storing_path = 'static\\pdf\\' + \
            image_path.split('\\')[-1].split('.')[0] + '.pdf'
        with open(storing_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
        return image_path.split('/')[-1].split('.')[0] + '.pdf'
    else:
        print(response.text)
        return None
        exit()

# Function to predict image given to it. It return the label of preditected output.


def predict(image_path):
    img = load_img(image_path, target_size=(100, 100))
    x = img_to_array(img)
    # Convert to grayscale channel
    x = rgb_to_grayscale(x)
    # Convert image shape to (100, 100, 1)
    x = np.expand_dims(x, axis=0)
    # Predict
    probability_of_prediction = loaded_model.predict(x)
    result = np.argmax(probability_of_prediction, axis=1)
    probability = round(probability_of_prediction[0][result][0] * 100, 2)
    result = ARRAY_OF_LABELS[result[0]]
    # class of image

    return result, probability


# Index page route is here.
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


# Upload route to upload any image on server, in the end it resized to 750 x 750 so that our canvas holds pixel values uniformaly
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['image']
        # Generating unqiue filename
        filename = str(uuid.uuid4())[:8] + f.filename
        rezied_filename = 'rezied' + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Saving the image
        f.save(os.path.join(filepath))
        # Peform OCR on image with help of API. It returns the pdf file name.
        pdf_path = convert_image_to_pdf(
            filepath, 'pdf_live_uVzdcGs0K6T6QZIAFuWD5knYNjCja1GrGYbVMPrHjpU')
        image = Image.open(filepath)
        # Resizing the image
        image = image.resize((750, 750))
        # Converting to RGB becuase jpg image does not support RGBA format.
        image = image.convert("RGB")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], rezied_filename))
        # Delete original image
        os.remove(filepath)
        # Resize image and save it to the upload folder
        return render_template('results.html', image_name=filename, rezied_filename=rezied_filename, pdf_file=pdf_path)


# Route used for prediction, any data sent to this route will convert the data into image for predictions.
@app.route('/predict', methods=['POST'])
def predict_image():
    if request.method == 'POST':
        # Get base64 data
        data = request.form['image_to_predict']
        # Decode base64 data
        with urllib.request.urlopen(data) as url:
            data = url.read()
        # Create filename
        filename = str(uuid.uuid4()) + '.png'
        print(filename)
        # Create filepath
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Save image to the filepath
        with open(filepath, 'wb') as f:
            f.write(data)
        # Predict image
        result, probability = predict(filepath)
        return jsonify(result=result, probability=probability)


if __name__ == '__main__':
    app.run(debug=True)
