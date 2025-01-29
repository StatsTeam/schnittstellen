from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int

BOOKS = [
    Book(id=1, title="Computer Science Pro", author="Jackson", description="A very nice book!", rating=5),
    Book(id=2, title="Be fast with FastAPI", author="Gandalf", description="A great book!", rating=5),
    Book(id=3, title="Master Endpoints", author="Jackson", description="An awesome book!", rating=5),
    Book(id=4, title="HP1", author="Author 1", description="Book Description", rating=2),
    Book(id=5, title="HP2", author="Author 2", description="Book Description", rating=3),
    Book(id=6, title="HP3", author="Author 3", description="Book Description", rating=1),
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create_book")
async def create_book(book_request: Book):
    BOOKS.append(book_request)