# Bumper Guestbook API

A Dockerized Django REST Framework API for creating guestbook entries and retrieving paginated entries and user-based message statistics.

Tech stack:

1. Python 3.12
2. Django
3. Django REST Framework
4. PostgreSQL
5. Docker
6. drf-spectacular (Swagger)

How to run:

1. Clone the repository:

git clone https://github.com/cagatayeralp/bumper-guestbook-api.git

2. Enter the project folder:

cd bumper-guestbook-api

3. Start the project:

docker compose --env-file .env.dev up --build

The API will be available at:

http://localhost:8000/api/

Swagger documentation:

http://localhost:8000/api/docs/

Run tests:

docker compose --env-file .env.dev exec web python manage.py test

View logs:

docker compose logs -f web

Filter application logs:

docker compose logs -f web | grep guestbook