# Fast_API_Quiz_project

To start project through the Docker you have to:

1) Build the Docker Images with:
    $ docker build -t db .
    $ docker build -t db_test .
2) Run containers based on your Images:
    $ docker-compose up --build

(Use 'sudo' in case of working on Linux)

To start the tests u have to:

1) Run containers based on your Images:
    $ docker-compose up --build
2) Enter the container:
    $ docker exec -it fast_api_project_app_1 bash
3) Start tests:
    $ python -m pytest


