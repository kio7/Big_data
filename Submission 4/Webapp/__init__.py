import sys
from functools import wraps
from operator import itemgetter

import bcrypt
from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, SubmitField, PasswordField

sys.path.append('../../')
from CassandraDB.connect_database import c_session
import requests
import re
from wtforms.validators import DataRequired

c_session = c_session


# Global variables for API. This is not a good practice, but it is a simple way to make the variables
# global without using a database or a config file.
class ApiVariables:
    def __init__(self) -> None:
        self.url = "http://localhost:5000/"
        self.key = "982734876345987234876345"  # API KEY
        # self.key = "123123qweqweqwerwer23423495"  # API KEY
        # self.headers = {"Authorization": f"ApiKey {self.key}"}
        self.headers = {"Authorization": self.key}


api = ApiVariables()

# Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key"

# Wrapper function to check is user is logged in.
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get("user_name"): # if user is not logged in, redirect to login page
            return redirect(url_for("login"))
        return func(*args, **kwargs) # if user is logged in, continue

    return decorated_function


# Flask routes -----------------------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    class LoginForm(FlaskForm):
        user_name = StringField('UserName', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Sign In')

    form = LoginForm()

    if request.method == "POST":
        username = request.form["user_name"]
        password = request.form["password"]
        bpw = bytes(password, 'utf-8')

        password = c_session.execute('SELECT password FROM users WHERE name = %s ALLOW FILTERING', (username,))
        if password:
            if bcrypt.checkpw(bpw, password[0].password):
                session["user_name"] = username
                return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Something went wrong. Please try again.", form=form)

    return render_template("login.html", form=form)


# Logout
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.pop("user_name", None)
    return redirect(url_for("login"))


# Home
@app.route("/home", methods=["GET"])
@login_required
def home():
    response = requests.get(api.url, headers=api.headers)
    if response.status_code == 200:
        data = response.json()
        return render_template("home.html", data=data)
    return render_template("home.html", data={"error": response.status_code, "": response.url})


# Collective route for all GET methods for books and cds.
@app.route("/search-library/", methods=["GET"])
@login_required
def search_library():

    flag = 1  # All Books and Cds
    name = None
    api_url = request.args.get('url')
    response = requests.get(api_url, headers=api.headers).json()

    if isinstance(response, dict):
        flag = 0  # All books or cds

        if "item_id" in response.keys():
            flag = 2  # Single book/cd
            name = list(response.keys())[0]  # key for Author/Creator/...

        elif "books" in response.keys():
            sorted_response = {"books": sorted(response["books"], key=itemgetter("item_id")),
                               "cds": sorted(response["cds"], key=itemgetter("item_id"))}
            response = sorted_response

    if isinstance(response, list):
        response.sort(key=itemgetter("item_id"))

    return render_template('search_library.html', response=response, flag=flag, name=name)


# Create a new book or cd.
@app.route("/submit/", methods=["GET", "POST"])
@login_required
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


# Edit an existing book or cd.
@app.route('/edit/', methods=["GET", "POST"])
@login_required
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


# Delete an existing book or cd.
@app.route("/delete/", methods=["GET"])
@login_required
def delete():
    api_url = request.args.get('url')
    redirect_category = request.args.get('category')
    requests.delete(api_url, headers=api.headers)
    return redirect(f"/search-library/?url={api.url}/{redirect_category}")


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
