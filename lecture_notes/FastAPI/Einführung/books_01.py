from fastapi import FastAPI, Body

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "history"},
    {"title": "Title Three", "author": "Author Three", "category": "math"},
    {"title": "Title Four", "author": "Author One", "category": "science"},
    {"title": "Title Six", "author": "Author Six", "category": "math"}
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

@app.get("/books/title_and_author/")
async def read_by_title_and_author(title: str, author: str):
    books_to_return = []
    for book in BOOKS:
        if book["title"].casefold() == title.casefold() and book["author"].casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/sorted/")
async def get_sorted_books(sort_by: str = "title"):
    if sort_by == "title":
        # Sort books by title:
        for i in range(len(BOOKS)):
            for j in range(i + 1, len(BOOKS)):
                if BOOKS[i]["title"] > BOOKS[j]["title"]:
                    BOOKS[i], BOOKS[j] = BOOKS[j], BOOKS[i]
    elif sort_by == "category":
        # Sort books by category:
        for i in range(len(BOOKS)):
            for j in range(i + 1, len(BOOKS)):
                if BOOKS[i]["category"] > BOOKS[j]["category"]:
                    BOOKS[i], BOOKS[j] = BOOKS[j], BOOKS[i]
    else:
        return {"error": "Invalid sort_by value. Use 'title' or 'category'."}
    
    return {"sorted_books": BOOKS}


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
