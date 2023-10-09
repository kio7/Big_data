import os
# from base64 import b64encode
# from io import BytesIO
# from PIL import Image
from flask import render_template
from forms import FileForm, ChoosePictureForm

# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans

# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
# import numpy as np
# import cv2

from baseconfig import app


def load_images_from_folder(folder_path):
    dataset = []
    filenames = []
    filepath = os.path.dirname(__file__) + folder_path
    for filename in os.listdir(filepath):
        if filename.endswith(".jpg"):
            img_path = os.path.join(filepath, filename)
            img = cv2.imread(img_path)
            if img is not None:
                # Resize the image to a common size if needed
                img = cv2.resize(img, (200, 100))
                img = img.reshape(-1)
                dataset.append(img)
                filenames.append(filename)
    return np.array(dataset), filenames


def load_images_segmentation(img_path):
    img_path = os.path.dirname(__file__) + img_path
    if img_path.endswith(".jpg"):
        img = cv2.imread(img_path)
        gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None and gray is not None:
            return img, gray


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/presentation", methods=["POST", "GET"])
def presentation():
    form = FileForm()


@app.route("/pattern-recognition", methods=["POST", "GET"])
def pattern_recognition():
    return render_template("pattern_recognition.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
