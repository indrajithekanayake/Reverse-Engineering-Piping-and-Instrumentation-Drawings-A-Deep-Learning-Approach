# load json and create model
import numpy as np
from keras.saving.model_config import model_from_json
from keras_preprocessing.image import load_img, img_to_array
from tensorflow import keras
from tensorflow.python.ops.image_ops_impl import rgb_to_grayscale

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

labels = ['Arrowhead', 'Arrowhead + Triangle', 'Box', 'Continuity Label',
          'Control', 'Control Valve Globe', 'DB&BBV', 'DB&BBV + Valve Check',
          'DB&BPV', 'ESDV Valve Ball', 'ESDV Valve Butterfly',
          'ESDV Valve Slab Gate', 'Exit to Atmosphere', 'Flange + Triangle',
          'Flange Joint', 'Flange Single T-Shape', 'Injector Point',
          'Reducer', 'Rupture Disc', 'Sensor', 'Spectacle Blind', 'Triangle',
          'Valve', 'Valve Angle', 'Valve Ball', 'Valve Butterfly',
          'Valve Check', 'Valve Globe', 'Valve Plug', 'Valve Slab Gate']

print(len(labels))


def predict(image_path):
    img = load_img(image_path, target_size=(100, 100))
    x = img_to_array(img)
    # Convert to grayscale channel
    x = rgb_to_grayscale(x)
    # Convert image shape to (100, 100, 1)
    x = np.expand_dims(x, axis=0)
    #
    print("Shape of image: ", x.shape)
    # Predict
    probability_of_prediction = loaded_model.predict(x)
    print("Predicted: ", probability_of_prediction)
    result = np.argmax(probability_of_prediction, axis=1)
    print("Probability: ", probability_of_prediction[0][result][0] * 100)
    result = labels[result[0]]
    return "Done"


predict('static/images/Capture (1).png')
