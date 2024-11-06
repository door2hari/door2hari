import numpy as np
import os
from flask import Flask,request,render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input

model = load_model(r"wcv.h5")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/input')
def input1():
    return render_template('input.html')

@app.route('/predict', methods=["GET", "POST"])
def res():
    if request.method == "POST":
        f = request.files['fileInput']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        f.save(filepath)
        print(filepath)
        img = image.load_img(filepath, target_size=(180,180))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        prediction = np.argmax(model.predict(x), axis=1)

        index = ['cloudy', 'foggy', 'rainy', 'shine', 'sunrise']

        result = str(index[prediction[0]])
        print(result)
        return render_template('output.html', prediction=result)


if __name__ == "__main__":
    app.run(host="localhost",debug=True)