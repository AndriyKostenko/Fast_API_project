# Fast_API_project

To start project through the Docker you have to:

1) Install all dependencies with:
    $ pip install -r requirements.txt

2) Build the Docker Image with:
    $ docker build -t myimage

3) Run container based on your image:
    $ docker run -p 8000:8000 myimage

(Use 'sudo' in case of working on Linux)
