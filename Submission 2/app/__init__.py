import os
from base64 import b64encode
from io import BytesIO
from PIL import Image
from flask import render_template, make_response
from pydicom import dcmread
from forms import PatterRecognitionForm, DICOMImageForm, DICOMDifferenceImageForm
import matplotlib.pyplot as plt
import numpy as np
import cv2
from dicom_to_numpy import dicom_to_numpy as dtn
from baseconfig import app
from pr_model import search_pr_model
from skimage.io import imread


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


@app.route("/pattern-recognition", methods=["POST", "GET"])
def pattern_recognition():
    form = PatterRecognitionForm()

    if form.submit.data and form.validate():
        image = form.picture.data
        image_raw = imread(os.path.join(os.path.dirname(__file__), "static/pr_images/", image))
        image_uri = os.path.join(os.path.dirname(__file__), "static/pr_images/", image)
        prediction = search_pr_model(image_raw)

        print(f"Denne: {prediction}")
        print(image_uri)
        return render_template(
            "pattern_recognition.html",
            form=form,
            image=image,
            prediction=prediction,
            submitted=1
        )

    return render_template("pattern_recognition.html", form=form, submitted=None)


@app.route("/dicom-pixel-data", methods=["POST", "GET"])
def dicom_pixel_data():
    form = DICOMImageForm()
    if form.submit.data and form.validate():
        img_path = os.path.dirname(__file__) + "/static/images/Dicom/" + form.picture.data
        data_set = dcmread(img_path)
        image, pixels = dtn(data_set)

        img = Image.fromarray(image, "L")
        image_io = BytesIO()
        img.save(image_io, "PNG")
        data_url = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
        return render_template("dicom_pixel_data.html", form=form, img=data_url, pixel_data=pixels, data_set=data_set,
                               submitted=1)
    return render_template("dicom_pixel_data.html", form=form, submitted=None)


@app.route("/difference_image", methods=["POST", "GET"])
def difference_image():
    form = DICOMDifferenceImageForm()
    if form.submit.data and form.validate():
        img_path = os.path.dirname(__file__) + "/static/images/Dicom/" + form.picture.data
        data_set = []
        image_set = []
        image_set_diff = []
        data_url_set = []
        for i in range(0, 5):
            file_name = form.picture.data
            file_name = "0" + str(int(file_name.split(".")[0]) + i) + ".dcm"
            img_path = os.path.dirname(__file__) + "/static/images/Dicom/" + file_name
            data_set.append(dcmread(img_path))
            image, pixels = dtn(data_set[i])
            image_set.append(image)
        for i in range(0, 3):
            diff_image = np.zeros((len(image_set[i]), len(image_set[i][0])), np.uint8)
            for j in range(0, len(image_set[i])):
                for k in range(0, len(image_set[i][j])):
                    if image_set[i][j][k] > image_set[i + 1][j][k]:
                        diff_image[j][k] = abs(image_set[i][j][k] - image_set[i + 1][j][k])
                    else:
                        diff_image[j][k] = abs(image_set[i + 1][j][k] - image_set[i][j][k])
            image_set_diff.append(diff_image)
        image_set_diff.insert(0, image_set[0])
        image_set_diff.append(image_set[4])
        for i in range(0, 5):
            img = Image.fromarray(image_set_diff[i], "L")
            image_io = BytesIO()
            img.save(image_io, "PNG")
            data_url = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            data_url_set.append(data_url)
        return render_template("difference_image.html", form=form, images=data_url_set, submitted=1)
    return render_template("difference_image.html", form=form, submitted=None)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
