from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

API_KEY = "your_api_key_here"

# Sample data (replace with your actual data)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
    # {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen"},
    # {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    # {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    # {"id": 7, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    # {"id": 8, "title": "Brave New World", "author": "Aldous Huxley"},
    # {"id": 9, "title": "Moby-Dick", "author": "Herman Melville"},
    # {"id": 10, "title": "The Odyssey", "author": "Homer"},
    # {"id": 11, "title": "War and Peace", "author": "Leo Tolstoy"},
    # {"id": 12, "title": "The Alchemist", "author": "Paulo Coelho"},
    # {"id": 13, "title": "The Shining", "author": "Stephen King"},
    # {"id": 14, "title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez"},
    # {"id": 15, "title": "The Hunger Games", "author": "Suzanne Collins"},
    # {"id": 16, "title": "The Da Vinci Code", "author": "Dan Brown"},
    # {"id": 17, "title": "The Road", "author": "Cormac McCarthy"},
    # {"id": 18, "title": "The Grapes of Wrath", "author": "John Steinbeck"},
    # {"id": 19, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson"},
    # {"id": 20, "title": "The Fault in Our Stars", "author": "John Green"},
    # {"id": 21, "title": "A Tale of Two Cities", "author": "Charles Dickens"},
    # {"id": 22, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling"},
    # {"id": 23, "title": "The Road Less Traveled", "author": "M. Scott Peck"},
    # {"id": 24, "title": "The Art of War", "author": "Sun Tzu"},
    # {"id": 25, "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky"},
    # {"id": 26, "title": "The Metamorphosis", "author": "Franz Kafka"},
    # {"id": 27, "title": "The Chronicles of Narnia", "author": "C.S. Lewis"},
    # {"id": 28, "title": "The Count of Monte Cristo", "author": "Alexandre Dumas"},
    # {"id": 29, "title": "The Picture of Dorian Gray", "author": "Oscar Wilde"},
    # {"id": 30, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
]

# Helper function to add HATEOAS links to a book
def add_links(book):
    book["links"] = [
        {"rel": "self", "href": url_for("get_book", book_id=book["id"], _external=True)},
        {"rel": "collection", "href": url_for("get_books", _external=True)}
    ]

def api_key_required(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        print(api_key)
        print(f"ApiKey {API_KEY}")
        if api_key and api_key == f"ApiKey {API_KEY}":
            return func(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    return wrapper


@app.route("/books", methods=["GET"])
# @api_key_required
def get_books():
    for book in books:
        add_links(book)
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        add_links(book)
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if "title" in data and "author" in data:
        new_book = {"id": len(books) + 1, "title": data["title"], "author": data["author"]}
        books.append(new_book)
        add_links(new_book)
        return jsonify(new_book), 201
    return jsonify({"error": "Invalid book data"}), 400

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

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
