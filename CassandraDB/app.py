import uuid

from flask import Flask
from connect_database import session

session = session
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # session.execute(
    #     """
    #     CREATE TABLE users (
    #         user_id uuid PRIMARY KEY,
    #         name text,
    #         credits int
    #     )
    #     """
    # )
    # session.execute(
    #     """
    #     INSERT INTO users (name, credits, user_id)
    #     VALUES (%s, %s, %s)
    #     """,
    #     ("John O'Reilly", 42, uuid.uuid1())
    # )
    rows = session.execute('SELECT user_id, name, credits FROM users')
    for row in rows:
        print(row.user_id, row.name, row.credits)

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
