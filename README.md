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

Pydantic sanitization

The API has 4 main endopioints:
- `/auth`
- `/user`
- `/book`
- `/author`


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

All the steps here were intended to a `bash` terminal.

This section shows how to run the project both with Docker or locally. Regardless of the method, start with the following steps:

1 - Clone the repo locally:
```bash
git clone https://github.com/lealre/madr-fastapi.git
```

2 - Access the project directory:
```bash
cd madr-fastapi
```

### Using Docker

[How to install Docker Compose](https://docs.docker.com/compose/install/)

To run this project using Docker, it's first necessary to set the environment variables in the `.env` file. An example of what this project uses can be found in the [.env-example](.env-example) file:
```
DATABASE_URL="postgresql+psycopg://app_user:app_password@madr_database:5432/app_db"

SECRET_KEY= 'your-secret-key'
ALGORITHM= 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES= 60
```

Copy these variables as they are and place them in your `.env` file and this will be enough to configure the project.

Once the variables in the `.env` file are defined, the following command will build and start the Docker containers with both PostgreSQL and the API running on localhost:
```bash
docker compose up --build -d
```

`--build` tells Docker Compose to build the images for the services defined in the docker-compose.yml file before starting the containers. If the images already exist and have not changed, Docker Compose will use the existing images. However, if there are changes in the Dockerfiles or in the context of the build (e.g., updated application code), this flag ensures that the images are rebuilt.

`-d` flag stands for "detached" mode, which means that Docker Compose will run the containers in the background. This allows you to continue using your terminal for other tasks while the containers run in the background.

You can access the Swagger documentation by navigating to the `/docs` endpoint in your browser:
```bash
http://localhost:8000/docs
```

This will open the interactive API documentation provided by Swagger.

### Locally

To run the project locally, the `.env` file is not strictly necessary, as it uses SQLite3 by default. All environment variables are configured to use standard values if the `.env` file is not set.

```python
# src/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str = 'sqlite:///database.db'
    SECRET_KEY: str = 'your-secret-key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
```

The project setup uses [`pyenv`](https://github.com/pyenv/pyenv) and [`poetry`](https://python-poetry.org/).

After completing steps 1 and 2:

3 - Set the Python version with `pyenv`:
```bash
pyenv local 3.12.2
```

4 - Create the virtual environment:
```bash
poetry env use 3.12.2
```

5 - Activate the virtual environment:
```bash
poetry shell
```

6 - Install dependencies:
```bash
poetry install
```

7 - Create the SQLite3 database locally:
```bash
alembic upgrade head
```

8 -Run the server:
```bash
task run
```

After these steps, you can access the Swagger documentation by navigating to the `/docs` endpoint in your browser:
```bash
http://localhost:8000/docs
```

This will open the interactive API documentation provided by Swagger.

**NOTES**

To run the tests, it is necessary to have Docker installed, as `testcontainers` builds a PostgreSQL instance for use.
```bash
task test
```

Before starting the tests, [Ruff](https://docs.astral.sh/ruff/) will detect format errors based on the points below:

- Import-related checks
- Flake8 style checks
- Error-related checks
- Warning-related checks
- Pylint-related checks
- Type-related checks, similar to Pylint

To automatically format the project based on these criteria, use:
```bash
task format
```

After running the tests, the coverage report is generated as an HTML file in `htmlcov/index.html`.

## Further Improvements

- Change the API to operate asynchronously.
- Create a simple front-end for user interaction.