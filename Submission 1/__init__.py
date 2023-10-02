from flask import render_template, redirect, url_for, flash
from forms import FileForm

from werkzeug.utils import secure_filename
import uuid
import os

from baseconfig import app


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/clustering", methods=["POST", "GET"])
def clustering():
    form = FileForm()
    if form.submit.data and form.validate():
        file_name = secure_filename(form.file_url.data.filename)
        file_name = str(uuid.uuid1()) + "_" + file_name
        form.file_url.data.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
        
        flash("File uploaded!", "success")
        return redirect(url_for("clustering"))

    return render_template("clustering.html", form=form)


@app.route("/segmentation", methods=["POST", "GET"])
def segmentation():
    return render_template("segmentation.html")



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
