# First API Project

This is a project to learn how to create a RESTful API using Flask and Flask-Smorest.

Tasks:

- Setup Mac Python Environment
- Install & Configure PostgreSQL
- Install & Configure Flask
- Install & Configure SQL Alchemy & Alembic
- Install & Configure Flask-Smorest
- Install & Configure Celery

Ref:

- https://rest-apis-flask.teclado.com/docs/course_intro/
- https://flask.palletsprojects.com/en/stable/
- https://flask-smorest.readthedocs.io/en/latest/

## Getting Start

1. Create `.env` file and fill in the value
2. Docker start the project `docker compose up --build`
3. Navigate to <http://localhost:5000/swagger-ui> to see the API documentation and perform testing.

## Development

1. To start the development server
   1. Build the docker image
   2. Run the container

```sh
docker build -t flask-smorest-api .
docker run --rm -d --name backend -p 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
```

2. Go to <http://localhost:5000/swagger-ui> to see the API documentation

| Method   | Endpoint            | Description                                             |
| -------- | ------------------- | ------------------------------------------------------- |
| ✅ GET    | /store/{id}/tag     | Get a list of tags in a store.                          |
| ✅ POST   | /store/{id}/tag     | Create a new tag.                                       |
| ✅ POST   | /item/{id}/tag/{id} | Link an item in a store with a tag from the same store. |
| ✅ DELETE | /item/{id}/tag/{id} | Unlink a tag from an item.                              |
| ✅ GET    | /tag/{id}           | Get information about a tag given its unique id.        |
| ✅ DELETE | /tag/{id}           | Delete a tag, which must have no associated items.      |
| POST     | /register            | Create user accounts given an email and password.       |
| POST     | /login               | Get a JWT given an email and password.                  |
| 🔒 POST  | /logout              | Revoke a JWT.                                           |
| 🔒 POST  | /refresh             | Get a fresh JWT given a refresh JWT.                    |
| GET      | /user/{user_id}      | (dev-only) Get info about a user given their ID.        |
| DELETE   | /user/{user_id}      | (dev-only) Delete a user given their ID.                |

### DB Related Operations

1. Create `migration` folder with `flask db init`

Everytime you make a change to the models, you need to run the following commands:

```sh
flask db migrate
flask db upgrade
```

To set the default value for the new column: [ref](https://rest-apis-flask.teclado.com/docs/flask_migrate/manually_review_modify_migrations/)

### Docker deploy

Start the services

```sh
docker compose up
```

Rebuild the image

```sh
docker compose up --build --force-recreate --no-deps web
```

