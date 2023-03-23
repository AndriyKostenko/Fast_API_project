# Fast_API_Quiz_project

Hello, this is my Quiz-project based on the following technologies:

 - Python3
 - FastApi
 - PostgreSQL
 - Docker
 - Docker-Compose
 - AWS + GitHubActions (for deploying)



# To start project through the Docker you have to:

1) `git clone https://github.com/AndriyKostenko/Fast_API_project.git` (copy the project)

2) `python3 -m venv venv` (installing virtual env.)

3) `source venv/bin/activate` (activate virtual env.)

4) `pip3 install -r requirements.txt` (installing all the requirements for the following project)
 
5) `docker compose up --build` (Build the Docker Image with Docker containers)

(Use 'sudo' in case of working on Linux)

# To start the tests u have to:

1) Run containers based on your Images:
    $ `docker-compose up --build`
2) Enter the container:
    $ `docker exec -it fast_api_project_app_1 bash`
3) Start tests:
    $ `python -m pytest`

![Screenshot from 2022-07-30 17-20-31](https://user-images.githubusercontent.com/91188777/181919480-cccf19b3-b297-4411-9edb-75600426686a.png)


