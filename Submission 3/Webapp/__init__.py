from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import requests


# To make the variables global.
class ApiVariables:
    def __init__(self) -> None:
        self.url = "http://localhost:5000/"
        self.key = "982734876345987234876345"  # API KEY
        # self.key = "123123qweqweqwerwer23423495"  # API KEY
        self.headers = {"Authorization": f"ApiKey {self.key}"}


api = ApiVariables()
app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key"


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("home"))


@app.route("/home", methods=["GET"])
def home():
    response = requests.get(api.url, headers=api.headers)
    if response.status_code == 200:
        data = response.json()
        return render_template("home.html", data=data)
    return render_template("home.html", data={"error": response.status_code, "": response.url})


@app.route("/search-library/", methods=["GET"])
def search_library():
    flag = 1  # All Books and Cds
    name = None
    api_url = request.args.get('url')
    response = requests.get(api_url, headers=api.headers).json()

    if isinstance(response, dict):
        flag = 0  # All books or cds
        if "id" in response.keys():
            flag = 2  # Single book/cd
            name = list(response.keys())[0]  # key for Author/Creator/...

    return render_template('search_library.html', response=response, flag=flag, name=name)


@app.route("/submit/", methods=["GET", "POST"])
def submit():
    rel = request.args.get('rel')
    api_url = request.args.get('url')
    json = request.args.get('json')

    class Form(FlaskForm):
        submit = SubmitField("Submit")

    form = Form()
    for e in json:
        setattr(form, e, StringField())

    return render_template("create.html", form=form)


@app.route("/delete/", methods=["GET"])
def delete():
    api_url = request.args.get('url')
    rel = request.args.get('category')
    requests.delete(api_url, headers=api.headers)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
