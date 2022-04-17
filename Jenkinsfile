pipeline {
    agent any
    
    environment {
        FASTAPI_DB_USER=credentials('fastapi-db-user')
        FASTAPI_DB_PASSWD=credentials('fastapi-db-passwd')
        FASTAPI_DB_NAME=credentials('fastapi-db')

        KEYCLOAK_DB_USER=credentials('keycloak-db-user')
        KEYCLOAK_DB_PASSWD=credentials('keycloak-db-passwd')
        KEYCLOAK_DB_NAME=credentials('keycloak-db')
    }

    stages {

        stage('Build-Checkout'){
            steps {
                // Get the code from the github repository
                git branch: 'main', url: 'https://github.com/pan-bellias/Reference-Letters-Server.git'  
            }
        }

        stage('Unit Testing') {
            steps {
                sh '''
                    python3.9 -m venv fvenv
                    source fvenv/bin/activate
                    pip install -r requirements.txt

                    cp ref_letters/.env.example ref_letters/.env
                    rm test.db || true
                    pytest
                   '''
            }
        }

        stage('E2E Testing') {
            steps {
                sh '''
                    echo "Unit test ready! E2E Testing awaits"
                   '''
            }
        }

        stage('Integration Testing') {
            steps {
                sh '''
                    echo "Integration testing awaits"
                   '''
            }
        }

        stage('UI Testing') {
            steps {
                sh '''
                    echo "UI testing awaits"
                   '''
            }
        }

        stage('Ansible Deployment') {

            environment {
                DB_URL=credentials('ansible-db-url')
            }

            steps {
                sshagent (credentials: ['ssh-ansible-vm']){
                sh '''
                    echo "Deployment with pure ansible needs testing"

                    cd ~/workspace/Ansible-Reference-Letter-Code
                    ansible-playbook -l ansible_group playbooks/postgres-install.yml \
                    -e PSQL_USER=$FASTAPI_DB_USER \
                    -e PSQL_PASSWD=$FASTAPI_DB_PASSWD \
                    -e PSQL_DB=$FASTAPI_DB_NAME

                    ansible-playbook -l ansible_group playbooks/postgres-install.yml \
                    -e PSQL_USER=$KEYCLOAK_DB_USER \
                    -e PSQL_PASSWD=$KEYCLOAK_DB_PASSWD \
                    -e PSQL_DB=$KEYCLOAK_DB_NAME

                    ansible-playbook -l ansible_group playbooks/keycloak-install.yml

                    ansible-playbook -l ansible_group playbooks/fastapi-install.yml \
                    -e DATABASE_URL=$DB_URL
                   '''
                }
            }
        }

        stage('Docker Deployment') {
            environment {
                DB_URL=credentials('docker-db-url')
                DOCKER_PASSWORD=credentials('docker-push-secret')
                DOCKER_USER=credentials('docker-user')
                DOCKER_PREFIX=credentials('docker-prefix-image-fastapi')
            }
            steps {
                sh '''
                    cd ~/workspace/Ansible-Reference-Letter-Code
                    ansible-playbook -l docker_group docker/install-docker.yml
                    ansible-playbook -l docker_group docker/fastapi-install.yml \
                    -e DATABASE_URL=$DB_URL
                   '''
                sh '''
                    cd ~/workspace/Reference-Letter-Server
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    docker build --rm -t $DOCKER_PREFIX:$TAG -t $DOCKER_PREFIX:latest -f fastapi.nonroot.Dockerfile . 
                   '''
                sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_PREFIX --all-tags
                   '''
                   
            }
        }

        stage('Helm Deployment') {
            steps {
                sh '''
                    echo "Deployment with helm chart awaits"
                   '''
            }
        }

        stage('Kubernetes Deployment') {
            steps {
                sh '''
                    echo "Deployment with kubernetes awaits"
                   '''
            }
        }
    }
}
    