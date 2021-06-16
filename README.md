# Containerized app deployment
This repository serves as a template to host your Python application in a Docker container as a microservice that can be accessed by REST API. 

## Structure
The folder structure for this project is as follows:

    .
    ├── app                     # FastAPI app files for the API endpoints
        ├── model               # App engine
            └── model.pickle    # Your model saved as pickle file
        └── main.py             # Definition HTTP methods
    ├── config                  # Configuration of NGINX in docker container

## Deployment
To deploy your app locally, follow the instructions below. For distribution purposes, it is convenient to link this GitHub repository to a DockerHub repository where you can store an image of your app that others can access directly. Follow [these instructions](https://docs.docker.com/docker-hub/builds/) to setup automated image building on DockerHub, based on changes to your GitHub repository, e.g. pushes to the master branch. 

### Locally
Running docker containers locally on non-Linux machines requires installation of [Docker Desktop](https://www.docker.com/products/docker-desktop) available for Mac and Windows. 

To build and spin up the API locally, navigate to the directory containing "docker-compose.yml" and run:

```bash
docker compose up --build
```

The API swagger documentation should become available at [http://localhost:8000/docs/](http://localhost:8000/docs/).