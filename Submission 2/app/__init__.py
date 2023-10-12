import os
from base64 import b64encode
from io import BytesIO
from PIL import Image
from flask import render_template, make_response, Response
from pydicom import dcmread
from forms import PatterRecognitionForm, DICOMImageForm, DICOMDifferenceImageForm
import matplotlib.pyplot as plt
import numpy as np
import cv2
from dicom_to_numpy import dicom_to_numpy as dtn
from baseconfig import app
from pr_model import search_pr_model
from skimage.io import imread
import time

differential_frame_data = None

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
        for i in range(0, 2):
            file_name = form.picture.data
            file_name = "0" + str(int(file_name.split(".")[0]) + i) + ".dcm"
            img_path = os.path.dirname(__file__) + "/static/images/Dicom/" + file_name
            data_set.append(dcmread(img_path))
            image, pixels = dtn(data_set[i])
            image_set.append(image)
        for i in range(0, 1):
            diff_image = np.zeros((len(image_set[i]), len(image_set[i][0])), np.uint8)
            for j in range(0, len(image_set[i])):
                for k in range(0, len(image_set[i][j])):
                    if image_set[i][j][k] > image_set[i + 1][j][k]:
                        diff_image[j][k] = abs(image_set[i][j][k] - image_set[i + 1][j][k])
                    else:
                        diff_image[j][k] = abs(image_set[i + 1][j][k] - image_set[i][j][k])
            image_set_diff.append(diff_image)
        image_set_diff.insert(0, image_set[0])
        #image_set_diff.append(image_set[4])
        for i in range(0, 2):
            img = Image.fromarray(image_set_diff[i], "L")
            image_io = BytesIO()
            img.save(image_io, "PNG")
            data_url = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            data_url_set.append(data_url)

        return render_template("difference_image.html", form=form, images=data_url_set,
                               pixel_data=image_set_diff[1], submitted=1)
    return render_template("difference_image.html", form=form, submitted=None)

@app.route('/pause_video_feed')
def pause_video_feed():
    global video_feed_paused
    video_feed_paused = True
    return "Video feed paused"

@app.route('/resume_video_feed')
def resume_video_feed():
    global video_feed_paused
    video_feed_paused = False
    return "Video feed resumed"

def generate_diff_frames():
    global differential_frame_data
    global video_feed_paused
    video_feed_paused = False

    vid_path = os.path.dirname(__file__) + "/static/images/video001_kort.mp4"
    cap = cv2.VideoCapture(vid_path)
    ret, prev_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        if video_feed_paused:
            time.sleep(0.3)
            continue
        ret, curr_frame = cap.read()
        if not ret:
            # Display a "Feed Ended" message on the last frame
            feed_ended_frame = np.zeros_like(prev_frame)
            cv2.putText(feed_ended_frame, "Feed Ended", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', feed_ended_frame)
            if not ret:
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            break

        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        differential_frame = cv2.absdiff(curr_frame_gray, prev_frame_gray)
        differential_frame_data = differential_frame

        ret, buffer = cv2.imencode('.jpg', differential_frame)
        if not ret:
            break

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        prev_frame_gray = curr_frame_gray


@app.route('/differential_video_feed')
def differential_video_feed():
    return Response(generate_diff_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/differential_video')
def differential_video():
    return render_template('differential_video.html')

@app.route('/get_differential_frame_data')
def get_differential_frame_data():
    global differential_frame_data  # Access the global differential frame data
    if differential_frame_data is not None:
        data = differential_frame_data.tolist()
        return str(data)
    return "No data available"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
