import click
import requests

API_URL = "http://localhost:5000"
API_KEY = "your_api_key_here"  # Replace with your API key


@click.group()
def cli():
    pass


headers = {"Authorization": f"ApiKey {API_KEY}"}


@cli.command()
def list_books():
    response = requests.get(f"{API_URL}/books", headers=headers)
    print(response)
    if response.status_code == 200:
        books = response.json()
        for book in books:
            print(f"Id: {book['id']}, Title: {book['title']}, Author: {book['author']}")
            for link in book['links']:
                print(f"  - {link['rel']}: {link['href']}")
    else:
        print("Failed to retrieve books.")


@cli.command()
@click.argument("book_id", type=int)
def get_book(book_id):
    response = requests.get(f"{API_URL}/books/{book_id}", headers=headers)
    if response.status_code == 200:
        book = response.json()
        print(f"Title: {book['title']}, Author: {book['author']}")
        for link in book['links']:
            print(f"  - {link['rel']}: {link['href']}")
    elif response.status_code == 404:
        print("Book not found.")
    else:
        print("Failed to retrieve book.")


@cli.command()
@click.option("--title", required=True, help="Title of the book")
@click.option("--author", required=True, help="Author of the book")
def create_book(title, author):
    data = {"title": title, "author": author}
    response = requests.post(f"{API_URL}/books", json=data)
    if response.status_code == 201:
        book = response.json()
        print(f"Created book with ID {book['id']}")
    else:
        print("Failed to create book.")


@cli.command()
@click.argument("book_id", type=int)
@click.option("--title", help="New title of the book")
@click.option("--author", help="New author of the book")
def update_book(book_id, title, author):
    data = {}
    if title:
        data["title"] = title
    if author:
        data["author"] = author
    response = requests.put(f"{API_URL}/books/{book_id}", json=data)
    if response.status_code == 200:
        book = response.json()
        print(f"Updated book with ID {book['id']}")
    elif response.status_code == 404:
        print("Book not found.")
    else:
        print("Failed to update book.")


@cli.command()
@click.argument("book_id", type=int)
def delete_book(book_id):
    response = requests.delete(f"{API_URL}/books/{book_id}")
    if response.status_code == 200:
        print("Deleted book successfully")
    elif response.status_code == 404:
        print("Book not found.")
    else:
        print("Failed to delete book.")


if __name__ == "__main__":
    cli()
