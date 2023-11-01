from flask import Flask, jsonify, request, url_for
from functools import wraps

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

# Sample data (replace with your actual data)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "status": 1},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "status": 1},
    # {"id": 3, "title": "1984", "author": "George Orwell", "status": 1},
    # {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "status": 1},
    # {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "status": 1},
    # {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien", "status": 1},
    # {"id": 7, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "status": 1},
    # {"id": 8, "title": "Brave New World", "author": "Aldous Huxley", "status": 1},
    # {"id": 9, "title": "Moby-Dick", "author": "Herman Melville", "status": 1},
    # {"id": 10, "title": "The Odyssey", "author": "Homer", "status": 1}
]
cds = [
    {"id": 1, "title": "Close to the Edge", "creator": "Yes", "status": 1},
    {"id": 2, "title": "Selling England by the Pound", "creator": "Genesis", "status": 1},
    # {"id": 3, "title": "The Dark Side of the Moon", "creator": "Pink Floyd", "status": 1},
    # {"id": 4, "title": "Fragile", "creator": "Yes", "status": 1},
    # {"id": 5, "title": "2112", "creator": "Rush", "status": 1},
    # {"id": 6, "title": "Thick as a Brick", "creator": "Jethro Tull", "status": 1},
    # {"id": 7, "title": "In the Court of the Crimson King", "creator": "King Crimson", "status": 1},
    # {"id": 8, "title": "Wish You Were Here", "creator": "Pink Floyd", "status": 1},
    # {"id": 9, "title": "Moving Pictures", "creator": "Rush", "status": 1},
    # {"id": 10, "title": "Hemispheres", "creator": "Rush", "status": 1}
]

# Helper function to add HATEOAS links to a book
def add_books_links(item):
    item["links"] = [
        {"rel": "books", "href": url_for("books_main", book_id=item["id"], _external=True), "method": "GET"},
    ]

def add_book_links(item):
    item["links"] = [
        # {"rel": "books", "href": url_for("get_book", book_id=item["id"], _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("books_main", book_id=item["id"], _external=True), "method": "DELETE"},
        {"rel": "books", "href": url_for("books_main", book_id=item["id"], _external=True), "method": "PUT", "json": ["title", "author"]},
    ]

def add_cds_links(item):
    item["links"] = [
        {"rel": "cd", "href": url_for("cd_main", cd_id=item["id"], _external=True), "method": "GET"},
    ]

def add_cd_links(item):
    item["links"] = [
        # {"rel": "cds", "href": url_for("get_cd", cd_id=item["id"], _external=True), "method": "GET"},
        {"rel": "cds", "href": url_for("cd_main", cd_id=item["id"], _external=True), "method": "DELETE"},
        {"rel": "cds", "href": url_for("cd_main", cd_id=item["id"], _external=True), "method": "PUT", "json": ["title", "creator"]}
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
    for book in books:
        add_books_links(book)
    for cd in cds:
        add_cds_links(cd)

    library = {
        "books": books, 
        "cds": cds,
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
            book = next((b for b in books if b["id"] == book_id), None)
            if book:
                add_book_links(book)
                return jsonify(book)
            return jsonify({"error": "Book not found"}), 404  
        else: 
            for book in books:
                add_books_links(book)
            return jsonify(books)

    if request.method == "POST":
        data = request.get_json()
        if "title" in data and "author" in data:
            new_book = {"id": len(books) + 1, "title": data["title"], "author": data["author"]}
            books.append(new_book)
            add_book_links(new_book)
            return jsonify(new_book), 201
        return jsonify({"error": "Invalid book data"}), 400
    
    if request.method == "PUT":
        data = request.get_json()
        if request.args.get('book_id'):
            book_id = int(request.args.get('book_id'))
            book = next((b for b in books if b["id"] == book_id), None)
            if book and "title" in data and "author" in data:
                book["title"] = data["title"]
                book["author"] = data["author"]
                return jsonify(book)
            return jsonify({"error": "Book not found or invalid data"}), 404

    if request.method == "DELETE":
        if request.args.get('book_id'):
            book_id = int(request.args.get('book_id'))
            book = next((b for b in books if b["id"] == book_id), None)
            if book:
                books.remove(book)
                return jsonify({"message": "Book deleted successfully"})
            return jsonify({"error": "Book not found"}), 404

# CDS
@app.route("/cds", methods=["GET", "POST", "PUT", "DELETE"])
@api_key_required
def cd_main():
    if request.method == "GET":
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = next((c for c in cds if c["id"] == cd_id), None)
            if cd:
                add_cd_links(cd)
                return jsonify(cd)
            return jsonify({"error": "CD not found"}), 404

        else:
            for cd in cds:
                add_cds_links(cd)
            return jsonify(cds)

    if request.method == "POST":
        data = request.get_json()
        if "title" in data and "creator" in data:
            new_cd = {"id": len(cds) + 1, "title": data["title"], "creator": data["creator"]}
            cds.append(new_cd)
            add_book_links(new_cd)
            return jsonify(new_cd), 201
        return jsonify({"error": "Invalid CD data"}), 400
    
    if request.method == "PUT":
        data = request.get_json()
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = next((c for c in cds if c["id"] == cd_id), None)
            if cd and "title" in data and "author" in data:
                cd["title"] = data["title"]
                cd["creator"] = data["creator"]
                return jsonify(cd)
            return jsonify({"error": "CD not found or invalid data"}), 404


    if request.method == "DELETE":
        if request.args.get("cd_id"):
            cd_id = int(request.args.get("cd_id"))
            cd = next((c for c in cds if c["id"] == cd_id), None)
            if cd:
                cds.remove(cd)
                return jsonify({"message": "CD deleted successfully"})
            return jsonify({"error": "CD not found"}), 404
    

if __name__ == "__main__":
    app.run(debug=True)
