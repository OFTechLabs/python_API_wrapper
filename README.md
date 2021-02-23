# Containerized app deployment
This repository serves as a template to host your Python application in a Docker container as a microservice that can be accessed by REST API. 

## Structure
The folder structure for this project is as follows:

    .
    ├── app                     # FastAPI app files for the API endpoints
        ├── model               # App engine
            └── model.pickle    # Your model saved as pickle file  
        └── main.py             # Definition HTTP methods


### Locally
In order to run the docker container locally on non-Linux machines one needs to install [Docker Desktop](https://www.docker.com/products/docker-desktop) available for Mac and Windows.  

In order to spin up a locally built version, navigate to the directory containing "docker-compose.yml" and run:

```bash
docker-compose up --build
```

The API swagger documentation should now be available at [http://localhost:80/docs/](http://localhost:5000/docs/).

