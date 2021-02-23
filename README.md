# Containerized app deployment
This repository serves as a template to host your Python application in a Docker container as a microservice that can be accessed by REST API. 

## Structure
The folder structure for this project is as follows:

    .
    ├── .github                 # Github specific files (Github Actions workflows)
    ├── app                     # FastAPI app files for the API endpoints
        ├── model               # App engine
        └── main.py             # Definition HTTP methods
    └── config                  # Configuration of NGINX in docker container


### Locally
In order to run the docker container locally on non-Linux machines one needs to install [Docker Desktop](https://www.docker.com/products/docker-desktop) available for Mac and Windows.  

To spin up a container based on the image in your DockerHub repository, open a command prompt or terminal window and use the following command: 

```bash
docker run -d -p 5000:8080 YourDockerHubAccountName/YourDockerHubRepository:latest
```

In order to spin up a locally built version, navigate to the directory containing "docker-compose.yml" and run:

```bash
docker-compose up --build
```

The API swagger documentation should now be available at [http://localhost:5000/docs/](http://localhost:5000/docs/).

