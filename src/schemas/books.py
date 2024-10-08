import re

from pydantic import BaseModel, Field, field_validator


class BookSchema(BaseModel):
    year: int = Field(gt=1700, lt=2025)
    title: str
    author_id: int = Field(gt=0)

    @field_validator('title')
    def validate_name(cls, v):
        v = v.lower().strip()
        return re.sub(r'\s+', ' ', v)


class BookPublic(BookSchema):
    id: int


class BookUpdate(BaseModel):
    year: int = Field(gt=0)


class BookList(BaseModel):
    books: list[BookPublic]
