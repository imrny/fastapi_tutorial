from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi import status


app = FastAPI()


books = [
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "published_date": "1925-04-10"
  },
  {
    "id": 2,
    "title": "Nineteen Eighty-Four",
    "author": "George Orwell",
    "published_date": "1949-06-08"
  },
  {
    "id": 3,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "published_date": "1960-07-11"
  }
]

@app.get("/")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{book_id} not found")

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: str

@app.post("/book")
def post_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class BookUpdate(BaseModel):
    title: str
    author: str
    published_date: str


@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    # for i, b in enumerate(books):
    #     if b["id"] == book_id:
    #         new_book = book.model_dump()
    #         books[i] = new_book
    #         books[i]["id"] = book_id
    #         return book

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{book_id} not found") 
    
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["published_date"] = book_update.published_date
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{book_id} not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
    return f"Book with Book ID:{book_id} deleted"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{book_id} not found")