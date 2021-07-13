from io import BytesIO
from flask import Flask, render_template, request, flash, redirect
from fastai.vision.all import *
from fastai.data.all import *
from fastai.data.external import *
from utils import img_to_price
import pathlib

# converting POSIX to WINDOWS path
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

UPLOAD_FOLDER = "./upload"
CLASSIFIER_MODEL_PATH = pathlib.Path(
    "D:\Machine Learning\Deep Learning\ChronoAnalyzer\models\classifier_stage1.pkl")
REGRESSOR_MODEL_PATH = pathlib.Path(
    r"D:\Machine Learning\Deep Learning\ChronoAnalyzer\models\regressor_stage2.pkl"
)
CLASSIFIER = load_learner(
    fname=CLASSIFIER_MODEL_PATH
)
REGRESSOR = load_learner(
    fname=REGRESSOR_MODEL_PATH, pickle_module=pickle
)
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def classifiy():
    return render_template("index.html")


@app.route("/prediction", methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        img = request.files['imgFile']

        if img.filename == '':
            message = "No Image Selected for Prediction."
            return render_template("index.html", message=message)

        if not allowed_file(img.filename):
            message = "Only JPG/JPEG/PNG files allowed."
            return render_template("index.html", message=message)

        img_bytes = img.read()
        image = tensor(Image.open(BytesIO(img_bytes)))
        prediction = CLASSIFIER.predict(image)
        price_prediction = REGRESSOR.predict(image)
        price_prediction = round(float(price_prediction[1]), 2)
        mapping = list(zip(
            CLASSIFIER.dls.vocab,
            [round(x, 4) for x in prediction[2].tolist()]
        ))
        mapping = sorted(mapping, key=lambda x: x[1], reverse=True)
        return render_template(
            "index.html", predictions=mapping[:4],
            prediction_price=price_prediction
        )


if __name__ == "__main__":
    app.run(debug=True)
