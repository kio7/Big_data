from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_KEY = "your_api_key_here"

def api_key_required(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        print(api_key)
        print(f"ApiKey {API_KEY}")
        if api_key and api_key == f"ApiKey {API_KEY}":
            return func(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return wrapper

# Sample data (replace with your actual data)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen"},
    # {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    # {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    # {"id": 7, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    # {"id": 8, "title": "Brave New World", "author": "Aldous Huxley"},
    # {"id": 9, "title": "Moby-Dick", "author": "Herman Melville"},
    # {"id": 10, "title": "The Odyssey", "author": "Homer"}
]
cds = [
    {"id": 1, "title": "CD1", "creator": "Musician1"},
    {"id": 2, "title": "CD2", "creator": "Musician2"},
    {"id": 3, "title": "CD3", "creator": "Musician3"},
    {"id": 4, "title": "CD4", "creator": "Musician4"},
]

# Helper function to add HATEOAS links to a book
def add_books_links(item):
    item["links"] = [
        {"rel": "self", "href": url_for("get_book", book_id=item["id"], _external=True), "method": "GET"},
        {"rel": "collection", "href": url_for("get_books", _external=True), "method": "GET"}
    ]

def add_book_links(item):
    item["links"] = [
        {"rel": "self", "href": url_for("get_book", book_id=item["id"], _external=True), "method": "GET"},
        {"rel": "collection", "href": url_for("get_books", _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("delete_book", book_id=item["id"], _external=True), "method": "DELETE"},
        {"rel": "books", "href": url_for("update_book", book_id=item["id"], _external=True), "method": "PUT", "json": ["title", "author"]}
    ]

def add_cds_links(item):
    item["links"] = [
        {"rel": "self", "href": url_for("get_cd", cd_id=item["id"], _external=True), "method": "GET"},
        {"rel": "collection", "href": url_for("get_cds", _external=True), "method": "GET"}
    ]

def add_cd_links(item):
    item["links"] = [
        {"rel": "self", "href": url_for("get_cd", cd_id=item["id"], _external=True), "method": "GET"},
        {"rel": "collection", "href": url_for("get_cds", _external=True), "method": "GET"},
        {"rel": "cds", "href": url_for("delete_cd", cd_id=item["id"], _external=True), "method": "DELETE"},
        {"rel": "cds", "href": url_for("update_cd", cd_id=item["id"], _external=True), "method": "PUT", "json": ["title", "creator"]}
    ]

# @api_key_required
@app.route("/", methods=["GET"])
def root():
    links = [
        {"rel": "library", "href": url_for("get_all", _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("get_books", _external=True), "method": "GET"},
        {"rel": "cds", "href": url_for("get_cds", _external=True), "method": "GET"},
        {"rel": "books", "href": url_for("create_book", _external=True), "method": "POST", "json": ["title", "author"]},
        {"rel": "cds", "href": url_for("create_cd", _external=True), "method": "POST", "json": ["title", "creator"]},

    ]
    return jsonify(links)


# @api_key_required
@app.route("/all", methods=["GET"])
def get_all():
    for book in books:
        add_books_links(book)
    for cd in cds:
        add_cd_links(cd)

    library = [{
        "books": books, 
        "cds": cds,
        }]
    return jsonify(library)

# @api_key_required
@app.route("/books", methods=["GET"])
def get_books():
    for book in books:
        add_books_links(book)
    return jsonify(books)

# @api_key_required
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        add_book_links(book)
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

#GET ROUTES
# @api_key_required
@app.route("/cds", methods=["GET"])
def get_cds():
    for cd in cds:
        add_cd_links(cd)
    return jsonify(cds)

# @api_key_required
@app.route("/cds/<int:cd_id>", methods=["GET"])
def get_cd(cd_id):
    cd = next((c for c in cds if c["id"] == cd_id), None)
    if cd:
        add_cd_links(cd)
        return jsonify(cd)
    return jsonify({"error": "CD not found"}), 404

# CREATE ROUTES
# @api_key_required
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if "title" in data and "author" in data:
        new_book = {"id": len(books) + 1, "title": data["title"], "author": data["author"]}
        books.append(new_book)
        add_book_links(new_book)
        return jsonify(new_book), 201
    return jsonify({"error": "Invalid book data"}), 400

# @api_key_required
@app.route("/cds", methods=["POST"])
def create_cd():
    data = request.get_json()
    if "title" in data and "creator" in data:
        new_cd = {"id": len(cds) + 1, "title": data["title"], "creator": data["creator"]}
        books.append(new_cd)
        add_book_links(new_cd)
        return jsonify(new_cd), 201
    return jsonify({"error": "Invalid CD data"}), 400

# UPDATE ROUTES
# @api_key_required
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    print(book_id)
    print(data)
    book = next((b for b in books if b["id"] == book_id), None)
    if book and "title" in data and "author" in data:
        book["title"] = data["title"]
        book["author"] = data["author"]
        return jsonify(book)
    return jsonify({"error": "Book not found or invalid data"}), 404

# @api_key_required
@app.route("/cds/<int:cd_id>", methods=["PUT"])
def update_cd(cd_id):
    data = request.get_json()
    print(cd_id)
    print(data)
    cd = next((c for c in books if c["id"] == cd_id), None)
    if cd and "title" in data and "author" in data:
        cd["title"] = data["title"]
        cd["creator"] = data["creator"]
        return jsonify(cd)
    return jsonify({"error": "CD not found or invalid data"}), 404

# DELETE ROUTES
# @api_key_required
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404

@app.route("/cds/<int:cd_id>", methods=["DELETE"])
# @api_key_required
def delete_cd(cd_id):
    cd = next((c for c in cds if c["id"] == cd_id), None)
    if cd:
        cds.remove(cd)
        return jsonify({"message": "CD deleted successfully"})
    return jsonify({"error": "CD not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
