https://rest-apis-flask.teclado.com/docs/course_intro/


## Development

1. To start the development server
   1. Build the docker image
   2. Run the container

```sh
docker build -t flask-smorest-api .
docker run --rm -d --name backend -p 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api
```

2. Go to <http://localhost:5000/swagger-ui> to see the API documentation

| Method | Endpoint            | Description                                             |
| ------ | ------------------- | ------------------------------------------------------- |
| ✅ GET    | /store/{id}/tag     | Get a list of tags in a store.                          |
| ✅ POST   | /store/{id}/tag     | Create a new tag.                                       |
| ✅ POST   | /item/{id}/tag/{id} | Link an item in a store with a tag from the same store. |
| ✅ DELETE | /item/{id}/tag/{id} | Unlink a tag from an item.                              |
| ✅ GET    | /tag/{id}           | Get information about a tag given its unique id.        |
| ✅ DELETE | /tag/{id}           | Delete a tag, which must have no associated items.      |