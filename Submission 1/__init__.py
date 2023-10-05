import os
from base64 import b64encode
from base64 import b64decode
from io import BytesIO
from PIL import Image
from flask import render_template, redirect, url_for, flash
from forms import FileForm
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import cv2


from baseconfig import app

def cluster_this(image_data):

    decoded_image = np.frombuffer(b64decode(image_data), dtype=np.uint8)
    img = cv2.imdecode(decoded_image, cv2.COLOR_BGR2RGB)
    
    # Splitting into channels
    blue, green, red = cv2.split(img)
    
    df_blue = blue/255
    df_green = green/255
    df_red = red/255

    pca_b = PCA(n_components=50)
    pca_b.fit(df_blue)
    trans_pca_b = pca_b.transform(df_blue)
    pca_g = PCA(n_components=50)
    pca_g.fit(df_green)
    trans_pca_g = pca_g.transform(df_green)
    pca_r = PCA(n_components=50)
    pca_r.fit(df_red)
    trans_pca_r = pca_r.transform(df_red)

    print(f"Blue Channel : {sum(pca_b.explained_variance_ratio_)}")
    print(f"Green Channel: {sum(pca_g.explained_variance_ratio_)}")
    print(f"Red Channel  : {sum(pca_r.explained_variance_ratio_)}")

    img_array = []

    fig_1 = plt.figure(figsize = (15, 7.2))
    plt.title("Blue Channel")
    plt.ylabel('Variation explained')
    plt.xlabel('Eigen Value')
    plt.bar(list(range(1,51)),pca_b.explained_variance_ratio_)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    image_data = np.array(bytearray(buf.read()), dtype=np.uint8)
    img_array.append(cv2.imdecode(image_data, cv2.IMREAD_COLOR))

    fig_2 = plt.figure(figsize = (15, 7.2))
    plt.title("Green Channel")
    plt.ylabel('Variation explained')
    plt.xlabel('Eigen Value')
    plt.bar(list(range(1,51)),pca_g.explained_variance_ratio_)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    image_data = np.array(bytearray(buf.read()), dtype=np.uint8)
    img_array.append(cv2.imdecode(image_data, cv2.IMREAD_COLOR))

    fig_3 = plt.figure(figsize = (15, 7.2))
    plt.title("Red Channel")
    plt.ylabel('Variation explained')
    plt.xlabel('Eigen Value')
    plt.bar(list(range(1,51)),pca_r.explained_variance_ratio_)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    image_data = np.array(bytearray(buf.read()), dtype=np.uint8)
    img_array.append(cv2.imdecode(image_data, cv2.IMREAD_COLOR))

    return [img_array]



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
    

        image =  decode_img(form.file_dump.data)    
        uri_original = f"data:image/png;base64,{image[1]}"
        cluster_images = cluster_this(image[0])
        
        return render_template("clustering.html", form=form, uri_original=uri_original, cluster_images=cluster_images)


    return render_template("clustering.html", form=form, uri_original='')


@app.route("/segmentation", methods=["POST", "GET"])
def segmentation():
    return render_template("segmentation.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
