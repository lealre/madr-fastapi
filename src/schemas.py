from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UsersList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class BookSchema(BaseModel):
    year: int = Field(gt=0)
    title: str
    author_id: int

    @field_validator('title')
    def validate_title(cls, v):
        return v.strip().lower()


class BookPublic(BookSchema):
    id: int


class BookUpdate(BaseModel):
    year: int = Field(gt=0)


class BookList(BaseModel):
    books: list[BookPublic]


class AuthorSchema(BaseModel):
    name: str

    @field_validator('name')
    def validate_name(clas, v):
        return v.strip().lower()


class AuthorPublic(AuthorSchema):
    id: int


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
