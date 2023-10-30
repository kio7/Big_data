from flask import Flask, render_template, redirect, url_for, request
import requests

# To make the variables global.
class ApiVariables:
    def __init__(self) -> None:
        self.url = "http://localhost:5000"
        self.key = "982734876345987234876345" # API KEY
        self.headers = {"Authorization": f"ApiKey {self.key}"}

api = ApiVariables()
app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key"


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("home"))


@app.route("/home", methods=["GET"])
def home():
    response = requests.get(f"{api.url}/", headers=api.headers)
    if response.status_code == 200:
        data = response.json()
        return render_template("home.html", data = data)
    return render_template("home.html", data={"error": response.status_code, "": response.url})


@app.route("/search-library/", methods=["GET"])
def search_library():

    api_url = request.args.get('url')
    response = requests.get(f"{api_url}", headers=api.headers).json()
    return render_template('search_library.html', response=response)


@app.route("/get/<rel>/<id>", methods=["GET"])
def get(rel, api_url, json, id = None):

    if id == None:
        response = requests.get(f"{api_url}", headers=api.headers)
        if response.status_code == 200:
            data = response.json()
            return render_template("list_all.html", data = data)
        
        books = response.json()
        return render_template("list_books.html", books=books)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
