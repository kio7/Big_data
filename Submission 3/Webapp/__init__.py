from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SubmitField
import re

import requests


# To make the variables global.
class ApiVariables:
    def __init__(self) -> None:
        self.url = "http://localhost:5000/"
        self.key = "982734876345987234876345"  # API KEY
        # self.key = "123123qweqweqwerwer23423495"  # API KEY
        # self.headers = {"Authorization": f"ApiKey {self.key}"}
        self.headers = {"Authorization": self.key}


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
    # Get the corresponding parameters to the item.
    json = request.args.get('json')
    temp = re.split(r'\W+', json)
    lis = []
    for e in temp:
        if e != '':
            lis.append(e)

    # Create dynamic form based on parameters above.
    class EntryForm(FlaskForm):
        entry = StringField()

    class MyForm(FlaskForm):
        """A form for one or more addresses"""
        field_list = FieldList(FormField(EntryForm), min_entries=1)
        submit = SubmitField("Create")

    columns = [{"name": x} for x in lis]
    form = MyForm(field_list=columns)

    # Create a new item.
    if form.validate_on_submit():
        api_url = request.args.get('url')
        data = {}
        for i in range(len(lis)):
            data[lis[i]] = form.field_list[i].data['entry']
        
        response = requests.post(api_url, json=data, headers=api.headers)
        if response.status_code == 201:
            return redirect(url_for('home'))

    # Change labels
    for i in range(len(columns)):
        form.field_list[i].entry.label = columns[i]['name']

    return render_template("create.html", form=form)


@app.route('/edit/', methods=["GET", "POST"])
def edit():
    # Get the corresponding parameters to the item.
    api_url = request.args.get('url')
    json = request.args.get('json')
    temp = re.split(r'\W+', json)
    lis = []
    for e in temp:
        if e != '':
            lis.append(e)

    # Create dynamic form based on parameters above.
    class EntryForm(FlaskForm):
        entry = StringField()

    class MyForm(FlaskForm):
        """A form for one or more addresses"""
        field_list = FieldList(FormField(EntryForm), min_entries=1)
        submit = SubmitField("Save")

    columns = [{"name": x} for x in lis]
    form = MyForm(field_list=columns)

    # Edit the existing item.
    if form.validate_on_submit():
        if request.args.get('id'):
            id = request.args.get('id')
            data = {}
            for i in range(len(lis)):
                data[lis[i]] = form.field_list[i].data['entry']
            data['id'] = id

            requests.put(api_url, json=data, headers=api.headers)
            return redirect(f"/search-library/?url={api_url}")
    
    # Edit labels and default values
    response = requests.get(api_url, headers=api.headers)
    if response.status_code == 200:
        data = response.json()
        for i in range(len(columns)):
            form.field_list[i].entry.label = columns[i]['name']
            form.field_list[i].entry.data = data[columns[i]['name']]
    
    return render_template('edit.html', form=form)


@app.route("/delete/", methods=["GET"])
def delete():
    api_url = request.args.get('url')
    redirect_category = request.args.get('category')
    requests.delete(api_url, headers=api.headers)
    return redirect(f"/search-library/?url={api.url}/{redirect_category}")


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
