![Build Status](https://github.com/OF-AVM-DK/ContainerizedAppDeployment/workflows/sphinx-autobuild/badge.svg)
![Build Status](https://github.com/OF-AVM-DK/ContainerizedAppDeployment/workflows/app-tests/badge.svg)

# Containerized app deployment
This repository serves as a template to host your Python application in a Docker container as a microservice that can be accessed by REST API. 

## Structure
The folder structure for this project is as follows:

    .
    ├── .github                 # Github specific files (Github Actions workflows)
    ├── app                     # FastAPI app files for the API endpoints
        ├── model               # App engine
        └── main.py             # Definition HTTP methods
    ├── config                  # Configuration of NGINX in docker container
    ├── docs                    # Sphinx documentation files (workflow builds html)
    └── test                    # Tests for app components (workflow runs all tests)

## Deployment
To deploy your app locally or on Amazon Web Services, follow the instructions below. For distribution purposes, it is convenient to link this GitHub repository to a DockerHub repository where you can store an image of your app that others can access directly. Follow [these instructions](https://docs.docker.com/docker-hub/builds/) to setup automated image building on DockerHub, based on changes to your GitHub repository, e.g. pushes to the master branch. 

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

### Deploy on Amazon Web Services
These instructions assume that you've installed and configured the Amazon [AWS CLI tools](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and the [ECS CLI tools](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_Configuration.html) with an IAM account that has at least write access to ECS and EC2 and the capability of creating AIM roles.

1. Configure the cluster. You can update the region and names as you see fit
```bash
ecs-cli configure --cluster yourapp-ecs-cluster --region eu-central-1 --config-name yourapp-ecs-conf --cfn-stack-name yourapp-ecs-stack --default-launch-type ec2
```
2. Create a new key pair. The result of this command is a key. Store this safely as you can later use it to access your instance through SSH.
```bash
aws ec2 create-key-pair --key-name yourapp
```
3. Create the instance that'll run the image. Here we used 1 server of type t2.medium. Change this as you see fit.
```bash
ecs-cli up --keypair yourapp --capability-iam --size 1 --instance-type t2.medium --cluster-config yourapp-ecs-conf
```
4. Update the server and make it run the docker image.
```bash
ecs-cli compose -f docker-compose_aws.yml up --cluster-config yourapp-ecs-conf
```
5. Now that the instance is running we can't access it yet. That's because NGINX only listens to localhost. We need to change this to make sure it's accessible on the web.
6. Login to the Amazon AWS console
7. Go to the EC2 service
8. In the instance list find the instance running the Docker image
9. Copy the public IP address of the instance
10. In ```config/api-nginx.conf``` update the server name to the public IP.
11. Now we need to rebuild and re-upload the image.
```bash
docker-compose -f docker-compose_aws.yml build --no-cache
docker-compose -f docker-compose_aws.yml push
ecs-cli compose -f docker-compose_aws.yml up --cluster-config yourapp-ecs-conf --force-update
```
12. You should now be able to access the API.

> :warning: This will make the API publicly available on the world wide web! Please note that this API is not protected in any way. Therefore it's recommended to run your instance in a private subnet and only access it through there. Alternatively you can change the security group settings to only allow incoming connections from your local IP or company VPN.  

## Documentation
The implementation of the API with Python package FastAPI ensures that Swagger UI documentation is readily available without additional steps. Please note that Swagger UI documentation assumes specific comment notation to extract the necessary information.  
Additionally, a GitHub workflow is setup such that a push to the master branch will rebuild Sphinx documentation from the files in the docs folder. The resulting html pages are located in the "gh-pages" branch. To host the Sphinx documentation from GitHub, go to Settings/GitHub Pages and select the "gh-pages" branch as Source. 

> :warning: Making your repository public will make it and its commit history available on the world wide web!

## Testing
The [pytest](https://docs.pytest.org/en/stable/) testing framework is used. Testing is performed automatically for pushes to the master branch based on tests located in the "tests" directory. Details on failed tests can be inspected further in the log files from the "Actions" menu. 
