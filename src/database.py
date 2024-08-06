from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


T_Session = Annotated[Session, Depends(get_session)]
