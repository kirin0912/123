from fastapi import FastAPI, HTTPException, Response

import database
from models import BookCreate, BookResponse

app = FastAPI(title="AI Books API")

database.init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Books API"}


@app.get("/books")
def list_books(skip: int = 0, limit: int = 10) -> list[BookResponse]:
    books = database.get_all_books(skip=skip, limit=limit)
    return [BookResponse(**b) for b in books]


@app.get("/books/{book_id}")
def get_book(book_id: int) -> BookResponse:
    book = database.get_book_by_id(book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book)


@app.post("/books", status_code=201)
def create_book(payload: BookCreate) -> BookResponse:
    if payload.title is None or payload.author is None or payload.price is None:
        raise HTTPException(status_code=422, detail="title, author, price are required")

    new_id = database.create_book(
        title=payload.title,
        author=payload.author,
        publisher=payload.publisher,
        price=payload.price,
        publish_date=payload.publish_date,
        isbn=payload.isbn,
        cover_url=payload.cover_url,
    )
    book = database.get_book_by_id(new_id)
    if book is None:
        raise HTTPException(status_code=500, detail="Create failed")
    return BookResponse(**book)


@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookCreate) -> BookResponse:
    current = database.get_book_by_id(book_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Book not found")

    title = payload.title if payload.title is not None else current["title"]
    author = payload.author if payload.author is not None else current["author"]
    price = payload.price if payload.price is not None else current["price"]
    publisher = payload.publisher if payload.publisher is not None else current["publisher"]
    publish_date = (
        payload.publish_date if payload.publish_date is not None else current["publish_date"]
    )
    isbn = payload.isbn if payload.isbn is not None else current["isbn"]
    cover_url = payload.cover_url if payload.cover_url is not None else current["cover_url"]

    ok = database.update_book(
        book_id=book_id,
        title=title,
        author=author,
        publisher=publisher,
        price=price,
        publish_date=publish_date,
        isbn=isbn,
        cover_url=cover_url,
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")

    book = database.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int) -> Response:
    ok = database.delete_book(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=204)
