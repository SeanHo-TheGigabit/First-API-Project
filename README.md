
https://rest-apis-flask.teclado.com/docs/course_intro/


## Development

1. To start the development server
   1. Build the docker image `docker build -t flask-smorest-api .`
   2. Run the container `docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api`
2. Go to <http://localhost:5000/swagger-ui> to see the API documentation