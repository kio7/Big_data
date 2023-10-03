from flask import render_template, redirect, url_for, flash
from forms import FileForm

# Other imports
from sklearn.decomposition import PCA, IncrementalPCA
from matplotlib.image import imread, imsave
import os


from baseconfig import app


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/clustering", methods=["POST", "GET"])
def clustering():
    form = FileForm()
    if form.submit.data and form.validate():
        image = form.file_dump.data
        
        img_raw = imread(image)

        # img_sum = img_raw.sum(axis=2)
        # img_bw = img_sum/img_sum.max()

        # pca = PCA()
        # pca.fit(img_bw)

        # # getting cumulative variance
        # var_cumu = np.cumsum(pca.explained_variance_ratio_)*100

        # # how many PCs explain 95% of the ratio ?
        # k = np.argmax(var_cumu>95)

        # ipca = IncrementalPCA(n_components=k)
        # img_recon = ipca.inverse_transform(ipca.fit_transform(img_bw))

        file_path = f"{app.config['UPLOAD_FOLDER']}/{image.filename}"
        imsave(file_path, img_raw)
    

        flash("Sending picture")
        return render_template("clustering.html", form=form, picture_src=file_path)

    return render_template("clustering.html", form=form, picture_src='')


@app.route("/segmentation", methods=["POST", "GET"])
def segmentation():
    return render_template("segmentation.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
