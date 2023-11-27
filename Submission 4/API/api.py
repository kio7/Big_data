import uuid

from flask import Flask, jsonify, request, url_for
from functools import wraps
import sys

sys.path.append('../../')
sys.path.append('../')
from CassandraDB.connect_database import c_session
from cassandra.query import dict_factory


c_session = c_session
c_session.row_factory = dict_factory
app = Flask(__name__)

API_KEY = "982734876345987234876345"


def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        # if api_key and api_key == f"ApiKey {API_KEY}":
        if api_key and api_key == API_KEY:
            return func(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401

    return wrapper


# Helper function to add HATEOAS links to a book
def add_books_links(item):
    item["links"] = [
        {"rel": "books", "href": url_for("books_main", book_id=item["item_id"], _external=True), "method": "GET"},
    ]


def add_book_links(item):
    item["links"] = [
        # {"rel": "books", "href": url_for("get_book", book_id=item["id"], _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("books_main", book_id=item["item_id"], _external=True), "method": "DELETE"},
        {"rel": "books", "href": url_for("books_main", book_id=item["item_id"], _external=True), "method": "PUT",
         "json": ["title", "author"]},
    ]


def add_cds_links(item):
    item["links"] = [
        {"rel": "cd", "href": url_for("cd_main", cd_id=item["item_id"], _external=True), "method": "GET"},
    ]


def add_cd_links(item):
    item["links"] = [
        # {"rel": "cds", "href": url_for("get_cd", cd_id=item["id"], _external=True), "method": "GET"},
        {"rel": "cds", "href": url_for("cd_main", cd_id=item["item_id"], _external=True), "method": "DELETE"},
        {"rel": "cds", "href": url_for("cd_main", cd_id=item["item_id"], _external=True), "method": "PUT",
         "json": ["title", "creator"]}
    ]


@app.route("/", methods=["GET"])
@api_key_required
def root():
    links = [
        {"rel": "library", "href": url_for("get_all", _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("books_main", _external=True), "method": "GET"},
        {"rel": "cds", "href": url_for("cd_main", _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("books_main", _external=True), "method": "POST", "json": ["title", "author"]},
        {"rel": "cds", "href": url_for("cd_main", _external=True), "method": "POST", "json": ["title", "creator"]},

    ]
    return jsonify(links)


@app.route("/all", methods=["GET"])
@api_key_required
def get_all():

    books2 = c_session.execute(
        """
        SELECT * FROM books
        """
    )
    cds2 = c_session.execute(
        """
        SELECT * FROM cds
        """
    )
    books3 = []
    cds3 = []
    for book in books2:
        add_books_links(book)
        books3.append(book)
    for cd in cds2:
        add_cds_links(cd)
        cds3.append(cd)

    library = {
        "books": books3,
        "cds": cds3,
    }
    # print(f"Library: \n -------- \n{jsonify(library)}")
    return jsonify(library)


# BOOKS
@app.route("/books", methods=["GET", "POST", "PUT", "DELETE"])
@api_key_required
def books_main():
    if request.method == "GET":
        if request.args.get('book_id'):
            book_id = int(request.args.get('book_id'))
            book = c_session.execute('SELECT * FROM books WHERE item_id = %s ALLOW FILTERING', [book_id])
            if book._current_rows:
                add_book_links(book[0])
                return jsonify(book[0])
            return jsonify({"error": "Book not found"}), 404
        else:
            books2 = c_session.execute(
                """
                SELECT * FROM books
                """
            )
            books3 = []
            for book in books2:
                add_books_links(book)
                books3.append(book)
            return jsonify(books3)

    if request.method == "POST":
        data = request.get_json()
        if "title" in data and "author" in data:
            booksees = c_session.execute('SELECT * FROM books')
            booksees = list(booksees)
            if booksees:
                booksees.sort(key=lambda x: x['item_id'])
                book_id = booksees[-1]['item_id'] + 1

            c_session.execute(
                """
                INSERT INTO books (id, item_id, title, author, status)
                VALUES (%s,%s, %s, %s, %s)
                """,
                (uuid.uuid1(), book_id, data['title'], data['author'], 1)
            )
            new_book = c_session.execute('SELECT * FROM books WHERE item_id = %s ALLOW FILTERING', [book_id])
            add_book_links(new_book[0])
            return jsonify(new_book[0]), 201
        return jsonify({"error": "Invalid book data"}), 400

    if request.method == "PUT":
        data = request.get_json()
        if request.args.get('book_id'):
            book_id = int(request.args.get('book_id'))
            book = c_session.execute('SELECT * FROM books WHERE item_id = %s ALLOW FILTERING', [book_id])
            if book._current_rows and "title" in data and "author" in data:
                c_session.execute(
                    """
                    UPDATE books SET title = %s, author = %s WHERE id = %s
                    """,
                    (data["title"], data["author"], book[0]['id'])
                )
                book[0]['title'] = data["title"]
                book[0]['author'] = data["author"]
                return jsonify(book[0])
            return jsonify({"error": "Book not found or invalid data"}), 404

    if request.method == "DELETE":
        if request.args.get('book_id'):
            book_id = int(request.args.get('book_id'))
            book = c_session.execute('SELECT * FROM books WHERE item_id = %s ALLOW FILTERING', [book_id])
            if book._current_rows:
                c_session.execute(
                    """
                    DELETE FROM books WHERE id = %s
                    """,
                    [book[0]['id']]
                )
                return jsonify({"message": "Book deleted successfully"})
            return jsonify({"error": "Book not found"}), 404


# CDS
@app.route("/cds", methods=["GET", "POST", "PUT", "DELETE"])
@api_key_required
def cd_main():
    if request.method == "GET":
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = c_session.execute('SELECT * FROM cds WHERE item_id = %s ALLOW FILTERING', [cd_id])
            if cd._current_rows:
                add_cd_links(cd[0])
                return jsonify(cd[0])
            return jsonify({"error": "CD not found"}), 404

        else:
            cds2 = c_session.execute(
                """
                SELECT * FROM cds
                """
            )
            cds3 = []
            for cd in cds2:
                add_cds_links(cd)
                cds3.append(cd)
            return jsonify(cds3)

    if request.method == "POST":
        data = request.get_json()
        if "title" in data and "creator" in data:
            ceedees = c_session.execute('SELECT * FROM cds')
            ceedees = list(ceedees)
            if ceedees:
                ceedees.sort(key=lambda x: x['item_id'])
                cd_id = ceedees[-1]['item_id'] + 1
            else:
                cd_id = 1
            c_session.execute(
                """
                INSERT INTO cds (id, item_id, title, creator, status)
                VALUES (%s,%s, %s, %s, %s)
                """,
                (uuid.uuid1(), cd_id, data['title'], data['creator'], 1)
            )
            new_cd = c_session.execute('SELECT * FROM cds WHERE item_id = %s ALLOW FILTERING', [cd_id])
            add_cd_links(new_cd[0])
            return jsonify(new_cd[0]), 201
        return jsonify({"error": "Invalid CD data"}), 400

    if request.method == "PUT":
        data = request.get_json()
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = c_session.execute('SELECT * FROM cds WHERE item_id = %s ALLOW FILTERING', [cd_id])
            if cd._current_rows and "title" in data and "creator" in data:
                c_session.execute(
                    """
                    UPDATE cds SET title = %s, creator = %s WHERE id = %s
                    """,
                    (data["title"], data["creator"], cd[0]['id'])
                )
                cd[0]['title'] = data["title"]
                cd[0]['creator'] = data["creator"]
                return jsonify(cd[0])
            return jsonify({"error": "CD not found or invalid data"}), 404

    if request.method == "DELETE":
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = c_session.execute('SELECT * FROM cds WHERE item_id = %s ALLOW FILTERING', [cd_id])
            if cd._current_rows:
                c_session.execute(
                    """
                    DELETE FROM cds WHERE id = %s
                    """,
                    [cd[0]['id']]
                )
                return jsonify({"message": "CD deleted successfully"})
            return jsonify({"error": "CD not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)
