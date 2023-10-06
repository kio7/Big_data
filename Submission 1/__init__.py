import os
from base64 import b64encode
from base64 import b64decode
from io import BytesIO
from PIL import Image
from flask import render_template, redirect, url_for, flash
from forms import FileForm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
import numpy as np
import cv2


from baseconfig import app


def load_images_from_folder(folder_path):
    dataset = []
    names = []
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
                names.append(filename)
    return np.array(dataset), names


def decode_img(form_data: FileForm) -> list:
    img = Image.open(form_data)
    data = BytesIO()
    img.save(data, "PNG")
    
    encoded_img = b64encode(data.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    
    return encoded_img, decoded_img


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/clustering", methods=["POST", "GET"])
def clustering():
    form = FileForm()
    if form.submit.data and form.validate():
    
        folder = form.folder.data
        data, names = load_images_from_folder(f"/static/photos/clustering/{folder}")

        # Folder path where JPG pictures are stored
        folder_path = "bilder"
        data, names = load_images_from_folder(folder_path)

        # Apply PCA to reduce dimensionality
        num_components = len(names)  # You can adjust this number based on your needs
        pca = PCA(n_components=num_components)
        data_pca = pca.fit_transform(data)

        # Perform clustering (K-Means in this example)
        num_clusters = 3  # You can adjust the number of clusters
        kmeans = KMeans(n_clusters=num_clusters)
        labels = kmeans.fit_predict(data_pca)

        # Visualize the clustered data
        plt.figure(figsize= (8, 6))
        colors = ["r", "b", "g"]
        for i in range(num_clusters):
            plt.scatter(data_pca[labels == i, 0], data_pca[labels == i, 1], c=colors[i % len(colors)], label=f"Cluster {i+1}")

        plt.title("PCA and K-Means Clustering")
        plt.legend()
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")


        return render_template("clustering.html", form=form, uri_original='', cluster_images = '')

        # image =  decode_img(form.file_dump.data)

        # uri_original = f"data:image/png;base64,{image[1]}"

        # cluster_images = cluster_this(image[0])
        # return render_template("clustering.html", form=form, uri_original=uri_original, cluster_images=cluster_images)

    return render_template("clustering.html", form=form, uri_original='', cluster_images = '')




@app.route("/segmentation", methods=["POST", "GET"])
def segmentation():
    return render_template("segmentation.html")


@app.route("/risikoanalyse", methods=["POST", "GET"])
def risikoanalyse():
    return render_template("risikoanalyse.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
