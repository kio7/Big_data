from flask import Flask, render_template, redirect, url_for

import requests

# To make the variables global.
class ApiVariables:
    def __init__(self) -> None:
        self.url = "http://localhost:5000"
        self.key = ""
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
        
        # links = []
        links = [{"link": "get"}, {}]
        for elm in data:
            match elm["method"]:
                case "GET": links.append({"link": "get", })
                case "POST": ...
                case "PUT": ...
                case "DELETE": ...

        return render_template("home.html", links=links)
    return render_template("home.html", data={"error": response.status_code, "": response.url})


@app.route("/get/<rel>/<id>", methods=["GET"])
def get(rel, id):
    response = requests.get(f"{api.url}/{...}", headers=api.headers)
    if response.status_code == 200:
        books = response.json()
        return render_template("list_books.html", books=books)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")