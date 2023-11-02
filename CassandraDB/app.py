import uuid
import hashlib
from flask import Flask
from connect_database import session
import bcrypt

session = session
app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "status": 1},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "status": 1},
    {"id": 3, "title": "1984", "author": "George Orwell", "status": 1},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "status": 1},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "status": 1},
    {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien", "status": 1},
    {"id": 7, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "status": 1},
    {"id": 8, "title": "Brave New World", "author": "Aldous Huxley", "status": 1},
    {"id": 9, "title": "Moby-Dick", "author": "Herman Melville", "status": 1},
    {"id": 10, "title": "The Odyssey", "author": "Homer", "status": 1}
]
cds = [
    {"id": 1, "title": "Close to the Edge", "creator": "Yes", "status": 1},
    {"id": 2, "title": "Selling England by the Pound", "creator": "Genesis", "status": 1},
    {"id": 3, "title": "The Dark Side of the Moon", "creator": "Pink Floyd", "status": 1},
    {"id": 4, "title": "Fragile", "creator": "Yes", "status": 1},
    {"id": 5, "title": "2112", "creator": "Rush", "status": 1},
    {"id": 6, "title": "Thick as a Brick", "creator": "Jethro Tull", "status": 1},
    {"id": 7, "title": "In the Court of the Crimson King", "creator": "King Crimson", "status": 1},
    {"id": 8, "title": "Wish You Were Here", "creator": "Pink Floyd", "status": 1},
    {"id": 9, "title": "Moving Pictures", "creator": "Rush", "status": 1},
    {"id": 10, "title": "Hemispheres", "creator": "Rush", "status": 1}
]


@app.route('/')
def hello_world():  # put application's code here
    # session.execute(
    #     """
    #     CREATE TABLE users (
    #         id uuid PRIMARY KEY,
    #         name text,
    #         password text,
    #         role_name text,
    #         role_id int
    #     )
    #     """
    # )

    # session.execute('DROP TABLE books')
    # session.execute('DROP TABLE cds')

    # books2 = session.execute('SELECT * FROM books')
    # for book in books2:
    #     print(type(book))

    # session.execute(
    #     """
    #     CREATE TABLE books (
    #         id uuid PRIMARY KEY,
    #         item_id int,
    #         title text,
    #         author text,
    #         status int
    #     )
    #     """
    # )
    #
    # session.execute(
    #     """
    #     CREATE TABLE cds (
    #         id uuid PRIMARY KEY,
    #         item_id int,
    #         title text,
    #         creator text,
    #         status int
    #     )
    #     """
    # )

    # password1 = b'admin'
    # hashed1 = bcrypt.hashpw(password1, bcrypt.gensalt())
    # password2 = b'member'
    # hashed2 = bcrypt.hashpw(password2, bcrypt.gensalt())
    # password3 = b'guest'
    # hashed3 = bcrypt.hashpw(password3, bcrypt.gensalt())

    # for book in books:
    #     session.execute(
    #         """
    #         INSERT INTO books (id, item_id, title, author, status)
    #         VALUES (%s, %s, %s, %s, %s)
    #         """,
    #         (uuid.uuid1(), int(book['id']), book['title'], book['author'], int(book['status']))
    #     )
    #
    # for cd in cds:
    #     session.execute(
    #         """
    #         INSERT INTO cds (id, item_id, title, creator, status)
    #         VALUES (%s,%s, %s, %s, %s)
    #         """,
    #         (uuid.uuid1(), int(cd['id']), cd['title'], cd['creator'], int(cd['status']))
    #     )

    # session.execute(
    #     """
    #     INSERT INTO users (id, name, password, role_name, role_id)
    #     VALUES (%s, %s, %s, %s, %s)
    #     """,
    #     (uuid.uuid1(), 'admin', hashed1, 'admin', 1)
    # )
    # session.execute(
    #     """
    #     INSERT INTO users (id, name, password, role_name, role_id)
    #     VALUES (%s, %s, %s, %s, %s)
    #     """,
    #     (uuid.uuid1(), 'member', hashed2, 'member', 2)
    # )
    # session.execute(
    #     """
    #     INSERT INTO users (id, name, password, role_name, role_id)
    #     VALUES (%s, %s, %s, %s, %s)
    #     """,
    #     (uuid.uuid1(), 'guest', hashed3, 'guest', 3)
    # )

    # password = session.execute('SELECT password FROM users WHERE name = %s ALLOW FILTERING', ('admin',))
    # if bcrypt.checkpw(b'admin', password[0].password):
    #     print('True')

    # rows = session.execute('SELECT user_id, name, credits FROM users')
    # for row in rows:
    #     print(row.user_id, row.name, row.credits)

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
