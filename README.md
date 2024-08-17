# MADR Backend API

This project consists of a backend API developed using [FastAPI](https://fastapi.tiangolo.com/) for a simplified version of a digital book collection.

It's called MADR (Mader), a Portuguese acronym for "Meu Acervo Digital de Romances" (My Digital Collection of Romances), and it allows user registration and all CRUD operations for both authors and books.

It is built using the FastAPI framework, with [Pydantic](https://docs.pydantic.dev/latest/) responsible for data validation. It uses a PostgreSQL database, and [SQLAlchemy](https://www.sqlalchemy.org/) is used for ORM, with [Alembic](https://alembic.sqlalchemy.org/en/latest/) handling database migrations during the development process.

It uses JWT authorization and authentication for the operations of creating, updating, and deleting records.

The tests have 100% coverage in the `src` folder using [pytest](https://docs.pytest.org/en/stable/) and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/). It also uses [factory-boy](https://factoryboy.readthedocs.io/en/stable/) to handle massive creation of models, [freezegun](https://github.com/spulec/freezegun) to test token expiration, and [testcontainers](https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/) to build a PostgreSQL instance during tests.

It is possible to run it locally using Docker Compose, which creates all the tables in PostgreSQL. A CI routine was also implemented using GitHub Actions.

## Table of Contents

- [Context](#context)
  - [Contract Schema](#contract-schema)
- [How it works](#how-it-works)
  - [Project Folder Structure](#project-folder-structure)
- [How to run this project](#how-to-run-this-project)
- [Further Improvements](#further-tasks)


## How it works

...


### Project Folder Structure
```
.
├── Dockerfile
├── README.md
├── alembic.ini
├── docker-compose.yaml
├── entrypoint.sh
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 5f80c5793a3a_create_users_table.py
│       ├── 7e20a64d10d4_create_authors_and_book_tables.py
├── poetry.lock
├── pyproject.toml
├── src
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── author.py
│   │   ├── books.py
│   │   └── users.py
│   ├── schemas
│   │   ├── authors.py
│   │   ├── base.py
│   │   ├── books.py
│   │   ├── token.py
│   │   └── users.py
│   ├── security.py
│   └── settings.py
└── tests
    ├── conftest.py
    ├── test_app.py
    ├── test_auth.py
    ├── test_author.py
    ├── test_book.py
    ├── test_security.py
    └── test_users.py
```
## How to run this project


## Further Improvements

- Change the API to operate asynchronously.
- Create a simple front-end for user interaction.