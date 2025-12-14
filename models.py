from pydantic import BaseModel, field_validator


class BookCreate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    price: int | None = None
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v <= 0:
            raise ValueError("price must be > 0")
        return v


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publisher: str | None
    price: int
    publish_date: str | None
    isbn: str | None
    cover_url: str | None
    created_at: str
