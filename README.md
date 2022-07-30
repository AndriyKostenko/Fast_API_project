# Fast_API_Quiz_project

Hello, this is my Quiz-project based on the following technologies:

 - Python3
 - FastApi
 - PostgreSQL
 - Docker
 - Docker-Compose
 - AWS + GitHubActions (for deploying)



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

![Screenshot from 2022-07-30 17-20-31](https://user-images.githubusercontent.com/91188777/181919480-cccf19b3-b297-4411-9edb-75600426686a.png)


