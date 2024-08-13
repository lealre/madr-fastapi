import re

from pydantic import BaseModel, field_validator


class AuthorSchema(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(cls, v):
        v = v.lower().strip()
        return re.sub(r'\s+', ' ', v)


class AuthorPublic(AuthorSchema):
    id: int


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
