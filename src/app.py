from fastapi import FastAPI

from src.routers import auth, author, books, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(author.router)


@app.get('/')
def home_root():
    return {'message': 'Root Endpoint!'}
