import os
from base64 import b64encode
from io import BytesIO
from PIL import Image
from flask import render_template
# , redirect, url_for
from forms import FileForm, ChoosePictureForm

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from Region_growing import region_growing

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2


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


@app.route("/clustering", methods=["POST", "GET"])
def clustering():
    form = FileForm()

    if form.submit.data and form.validate():

        # Folder path where JPG pictures are stored
        # Additional datasets can be placed here. Only jpeg support.
        folder:str = form.folder.data 
        # ----------------------------------------
        clusters:int = form.clusters.data
        show_filenames:bool = form.show_filenames.data 
        data, filenames = load_images_from_folder(f"/static/photos/clustering/{folder}")
        

        # Apply PCA to reduce dimensionality
        num_components = len(filenames)  # You can adjust this number based on your needs
        pca = PCA(n_components=num_components)
        data_pca = pca.fit_transform(data)

        # Perform K-means clustering
        num_clusters = clusters  # Adjust the number of clusters
        kmeans = KMeans(n_clusters=num_clusters)
        labels = kmeans.fit_predict(data_pca)

        # Visualize the clustered data using matplotlib
        fig = Figure(figsize=(8, 6))
        plot = fig.subplots()

        colors = ["c", "m", "y", "k", "r", "b", "g", "#FF00FF"]
        cluster_display_images = {}

        for i in range(num_clusters):
            cluster_data = data_pca[labels == i]
            cluster_filenames = [filenames[j] for j in range(len(filenames)) if labels[j] == i]
            cluster_display_images[i] = sorted(cluster_filenames)

            if show_filenames:
                plot.scatter(cluster_data[:, 0], cluster_data[:, 1], c=colors[i % len(colors)], label=f"Cluster {i+1}")
                for j in range(len(cluster_filenames)):
                    plot.annotate(cluster_filenames[j], (cluster_data[j, 0], cluster_data[j, 1]))
            else:
                plot.scatter(
                    data_pca[labels == i, 0],
                    data_pca[labels == i, 1],
                    c=colors[i % len(colors)],
                    label=f"Cluster {i+1}",
                )
        print(cluster_display_images)

        plot.set_title("PCA and K-Means Clustering")
        plot.legend()
        plot.set_xlabel("Principal Component 1")
        plot.set_ylabel("Principal Component 2")

        # Save plot to variabel
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = b64encode(buf.getvalue()).decode("utf-8")
        plot_image = f"data:image/png;base64,{data}"

        return render_template(
            "clustering.html",
            form=form,
            plot_image=plot_image,
            folder=folder,
            filenames=sorted(filenames),
            cluster_display_images = cluster_display_images,
            show_filenames=show_filenames,
        )

    return render_template("clustering.html", form=form, uri_original="", plot_image="")


@app.route("/segmentation", methods=["POST", "GET"])
def segmentation():
    form = ChoosePictureForm()
    if form.submit.data and form.validate():
        # Folder path where pictures are stored
        picture_name = form.picture.data
        # Threshold set by user
        threshold = form.threshold.data
        img_thres, gray = load_images_segmentation(f"/static/photos/segmentation/{picture_name}")

        plt.switch_backend("agg")

        # Region growing
        # Seed point is in the middle of the picture.
        seed_point = (gray.shape[0] // 2, gray.shape[1] // 2)
        # threshold = 80
        img_region_grow = region_growing(gray, seed_point, threshold)
        plt.imshow(img_region_grow)
        buf = BytesIO()
        plt.savefig(buf)
        data = b64encode(buf.getvalue()).decode("utf-8")
        img_rg = f"data:image/png;base64,{data}"

        # Thresholding
        img_blured = cv2.medianBlur(gray, 5)
        img_thres = cv2.adaptiveThreshold(img_blured, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        plt.imshow(img_thres)
        buf2 = BytesIO()
        plt.savefig(buf2)
        data = b64encode(buf2.getvalue()).decode("utf-8")
        img_thres = f"data:image/png;base64,{data}"

        # Watershed

        return render_template(
            "segmentation.html",
            form=form,
            flag=True,
            picture_name=picture_name,
            img_rg=img_rg,
            img_thres=img_thres,
        )

    return render_template("segmentation.html", form=form, flag=False)


@app.route("/risikoanalyse", methods=["POST", "GET"])
def risikoanalyse():
    return render_template("risikoanalyse.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
