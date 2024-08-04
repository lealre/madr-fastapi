from fastapi import FastAPI

from src.routers import users

app = FastAPI()

app.include_router(users.router)


@app.get('/')
def home_root():
    return {'message': 'Root Endpoint!'}
