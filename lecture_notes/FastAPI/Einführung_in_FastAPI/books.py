from fastapi import FastAPI, Body

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author One", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"}
]

app = FastAPI()

@app.get("/books/id/{book_id}")
async def read_by_index(book_id: int):
    return BOOKS[book_id]

@app.get("/books/title/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/category/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/category_and_author/{book_author}/")
async def read_by_category_and_author_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == book_author.casefold() and book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)

@app.put("/books/update_book")
async def update_book(updatd_request=Body()):
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == updatd_request["title"].casefold():
            BOOKS[index] = updatd_request

@app.delete("/book/delete_book/{book_title}")
async def delete_book(book_title: str):
    for index, book in enumerate(BOOKS):
        if book["title"].casefold() == book_title.casefold():
            BOOKS.pop(index)
            break