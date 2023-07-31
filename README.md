# Y_Lab FastAPI project

[![python](https://img.shields.io/badge/python-3.9-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.100.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![pytest](https://img.shields.io/badge/pytest-passed-brightgreen)](https://docs.pytest.org/en/7.4.x/)


## Description:

FastAPI educational project for Y_Lab. This is a backend service for restaurants with CRUD menu operations. There are three entities: Menu, Submenu, Dishes.
The documentation can be found at (http://0.0.0.0:8000/docs,
http://localhost:8000/docs or http://127.0.0.1:8000/docs)


## Based on:
- Python 3.9
- FastAPI 0.89.1
- SQLAlchemy 2.0.19
- Alembic 1.11.1
- Gunicorn 21.2.0
- PostgreSQL 15.1-alpine


## How to use it

```shell
git clone https://github.com/cnwv/FastAPI_project_Y_Lab.git

cd FastAPI_project_Y_Lab

docker-compose up -d
```

## How to test it
### Pytest
```shell
docker-compose up -d
docker exec -it fastapi_app pytest -v
```

### Postman
Upload the menu app.postman_environment.json and menu app.postman_collection.json files from the /tests/postman folder to postman and run the test.
