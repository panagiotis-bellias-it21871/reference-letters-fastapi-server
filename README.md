# Reference-Letters-Server
An application about reference letter handling in the context of DIT HUA Thesis 'Usage of devops tools and methodologies in development and productivity of web apps'

## Installation
```bash
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

# DOCKER NETWORK
```bash
docker network create reference-letters-network
docker network inspect reference-letters-network
docker network connect reference-letters-network reference-letters-server-nginx-1
docker network connect reference-letters-network reference-letters-frontend-app
```