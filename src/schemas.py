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
    year: int | None = Field(gt=0, default= None)
    title: str | None = None
    author_id: int | None = None

    @field_validator('title')
    def validate_title(cls, v):
        return v.strip().lower()


class BookList(BaseModel):
    books: list[BookPublic]
