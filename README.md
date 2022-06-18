# reference-letters-fastapi-server
A back end web application about reference letter handling in the context of DIT HUA Thesis "Use of devops methodologies and tools in development and production environment of web applications"

<p align="left"> <img src="https://komarev.com/ghpvc/?username=panagiotis-bellias-it21871&label=Profile%20views&color=0e75b6&style=flat" alt="panagiotis-bellias-it21871" /> </p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
</p>

<a name="contents"></a>
## Table Of Contents
1. [Table Of Contents](#contents)  
2. [Run Project Locally (Installation)](#locally)  
3. [Deploy fastapi project to a VM (Virtual Machine)](#deployment)  
3.1. [CI/CD tool configuration (Jenkins Server)](#jenkins)
3.2. [Deployment with Docker and docker-compose using Ansible](#docker)  
...

<a name="locally"></a>
## Run Project Locally (Installation)

### Clone and initialize project
```bash
git clone https://github.com/panagiotis-bellias-it21871/reference-letters-fastapi-server.git
virtualenv fvenv -p python3.X
source fvenv/bin/activate
pip install -r requirements.txt
```
and
```bash
cp ref_letters/.env.example ref_letters/.env
```
editting .env file to define
```vim
DATABASE_URL=sqlite:///./dev.db
KC_SERVER_URL="https://auth.some-domain.com/auth"
KC_CLIENT_ID="test-client"
KC_REALM="Test"
KC_CLIENT_SECRET="GzgACcJzhzQ4j8kWhmhazt7WSdxDVUyE"
```
or
```bash
cp ref_letters/.env.docker.example ref_letters/.env
```
```vim
DATABASE_URL=postgresql://<DB-USERNAME>:<DB-PASSWORD>@localhost:5432/<DB-NAME>
KC_SERVER_URL="http://keycloak_auth:8085/auth/"
KC_CLIENT_ID="fastapi-service"
KC_REALM="Clients"
KC_CLIENT_SECRET="GzgACcJzhzQ4j8kWhmhazt7WSdxDVUyE"
```
in case you want to use postgresql either you are in a docker environment or not. First you should have created a database using [pgAdmin](https://www.youtube.com/watch?v=1wvDVBjNDys) or command line.
The other variables are referred in keycloak usage where you should suit them according to the environment where keycloak service is running.

### Run application server
```bash
uvicorn ref_letters.main:app --reload
```

[See what you have done](http://127.0.0.1:8080/)

<a name="deployment"></a>
## Deploy fastapi project to a VM (Virtual Machine)

We are going to need 4 VMs. One for the jenkins server and one for each execution environment (ansible, docker and
kubernetes)

* [Create VM in Azure Portal](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal)
* [SSH Access to VMs](https://help.skytap.com/connect-to-a-linux-vm-with-ssh.html)
* [SSH Automation](https://linuxize.com/post/using-the-ssh-config-file/)
* [Reserve Static IP in Azure](https://azure.microsoft.com/en-au/resources/videos/azure-friday-how-to-reserve-a-public-ip-range-in-azure-using-public-ip-prefix/)

<a name="jenkins"></a>
### CI/CD tool configuration (Jenkins Server)

* [Install Jenkins](https://www.jenkins.io/doc/book/installing/linux/)

Make sure service is running
```bash
sudo systemctl status jenkins
netstat -anlp | grep 8080 # needs package net-tools
```

<a name="conf_shell"></a>
#### Step 1: Configure Shell
Go to Dashboard / Manage Jenkins / Configure System / Shell / Shell Executable and type '/bin/bash'

<a name="webhooks"></a>
#### Step 2: Add webhooks both to fastapi and ansible repositories
[Dublicate](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/duplicating-a-repository) repositories for easier configuration.

* [Add Webhooks - see until Step 4](https://www.blazemeter.com/blog/how-to-integrate-your-github-repository-to-your-jenkins-project)

<a name="credentials"></a>
#### Step 3: Add the credentials needed

* [Add SSH keys & SSH Agent plugin](https://plugins.jenkins.io/ssh-agent/) with id 'ssh-ansible-vm' to access
ansible-vm, and 'ssh-docker-vm' to access docker-vm
* [Add Secret Texts](https://www.jenkins.io/doc/book/using/using-credentials/) for every environmental variable we
need to define in our projects during deployment, like below

```nano
# ID                        What is the value?
ansible-db-url              <value>
docker-db-url
docker-push-secret
docker-user
docker-prefix-image-fastapi
fastapi-db-user
fastapi-db-passwd
fastapi-db
keycloak-db-user
keycloak-db-passwd
keycloak-db
etc.
```

<a name="jobs"></a>
#### Create Jobs
* [Create Freestyle project for Ansible code](https://www.guru99.com/create-builds-jenkins-freestyle-project.html)
* [More for Ansible](https://github.com/pan-bellias/Ansible-Reference-Letter-Code.git)
* [Create Pipeline project](https://www.jenkins.io/doc/pipeline/tour/hello-world/)
* [Add Webhooks to both jobs - see until Step 9](https://www.blazemeter.com/blog/how-to-integrate-your-github-repository-to-your-jenkins-project)

In the fastapi job the pipeline will be the [Jenkinsfile](Jenkinsfile)

<a name="build"></a>
##### Build-Checkout stage
Takes the code from the git repository

<a name="test"></a>
##### Unit Test stage
Activates a virtual environment, installs the requirements, copies the .env.example to use it as .env with some
demo values for testing and uses pytest so the application can be tested before goes on production.
NOTE: connect to your jenkins vm and do the below line so the test stage can run
```bash
<username>@<vm-name>:~$ sudo apt-get install libpcap-dev libpq-dev
```

##### E2E Testing
##### Integration Testing
##### UI Testing

<a name="j-ansible"></a>
##### Ansible Deployment
Ansible connects to the ansible-vm through ssh agent and the ssh key we define there and runs a playbook for
postgres database configuration, keycloak and fastapi service configuration passing the sensitive parameters from secret texts.

<a name="j-docker"></a>
##### Docker Deployment
Ansible connects to the docker-vm through ssh and runs a playbook that it will define the sensitive parameters and
will use docker-compose module to do docker-compose up the containers according to [docker-compose.yml](docker-compose.yml)

<a name="j-k8s-pre"></a>
##### Preparing k8s Deployment
Here, to deploy our app we need a docker image updated. So we build the image according to [nonroot.Dockerfile](nonroot.Dockerfile), we are logging in Dockerhub and push the image there to be public available.

<a name="j-k8s"></a>
##### Kubernetes Deployment
After we have [configure connection](https://github.com/pan-bellias/Reference-Letters-Service#connect-kubernetes-cluster-with-local-pc-orand-jenkins-server)
between jenkins user and our k8s cluster, we update secrets and configmaps using also some Ansible to populate ~/.
env values and create all the needed entities such as persistent volume claims, deployments, cluster IPs, ingress,
services.

Secrets and ConfigMaps could be just prepared from earlier. This is applied to the https ingress, we will see
later in [SSL configuration](https://github.com/pan-bellias/Reference-Letters-Service#in-kubernetes-environment)

<a name="ansible"></a>
### Deployment with pure Ansible
In order to be able to use Ansible for automation, there is the [ansible-reference-letter-project](https://github.com/pan-bellias/Ansible-Reference-Letter-Code.git). There is installation and usage guide.

* [More Details](https://github.com/pan-bellias/Ansible-Reference-Letter-Code#pure-ansible)

<a name="docker"></a>
### Deployment with Docker and docker-compose using Ansible
In order to deploy our project in Docker environment, we use again the [ansible-reference-letter-project](https://github.com/pan-bellias/Ansible-Reference-Letter-Code.git) where we use a playbook that uses an Ansible role to run the application
with docker-compose according to the [docker-compose.yml](docker-compose.yml). In that file, we have defined three
services, the postgres container with its volume in order to be able to store data, the keycloak container (information is missing) and the fastapi container for our
app taking environmental variables from local .env file (it's ready when we run the playbook from jenkins-server
where the sensitive values from environmental variables are parametric). The fastapi container is built according
to the [nonroot.Dockerfile](nonroot.Dockerfile) as a nonroot process for safety reasons.

* [More Info Here](https://github.com/pan-bellias/Ansible-Reference-Letter-Code#ansible--docker)

#### Docker Network
```bash
docker network create reference-letters-network
docker network inspect reference-letters-network
docker network connect reference-letters-network reference-letters-server_fastapi_1
docker network connect reference-letters-network reference-letters-frontend-app # we will see that
```

#### Docker Images - GitHub Container Registry

* [Link for Info](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

```bash
# build image
docker build . -t ghcr.io/pan-bellias/ref-letters-server:latest -f fastapi.nonroot.Dockerfile
# push image
docker push ghcr.io/pan-bellias/ref-letters-server:latest
```

