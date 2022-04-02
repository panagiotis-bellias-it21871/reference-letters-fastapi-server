pipeline {
    agent any
    
    stages {
        stage('Build'){
            steps {
              // Get some code from a GitHub repository
                git branch: 'main', url: 'https://github.com/pan-bellias/Reference-Letters-Server'  
            }
        }
        stage('Test') {
            steps {
                sh '''
                    python3.9 -m venv fvenv
                    source fvenv/bin/activate
                    pip install -r requirements.txt
                    cp .env.example .env
                    rm test.db || true
                    pytest
                   '''
            }
        }
        stage('Ansible Deployment') {
            steps {
                sh '''
                   '''
            }
        }
        stage('Docker Deployment') {
            environment {
                DOCKER_PASSWORD = credentials('docker-push-secret')
                DOCKER_USER = 'bellias'
                DOCKER_PREFIX = 'bellias/reflettersserver'
            }
            steps {
                sh '''
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    docker build --rm -t $DOCKER_PREFIX:$TAG -t $DOCKER_PREFIX:latest -f nonroot.Dockerfile . 
                   '''
                sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_PREFIX --all-tags
                   '''
                   
            }
        }
        stage('Kubernetes Deployment') {
            steps {
                sh '''
                   '''
            }
        }
        stage('Helm Deployment') {
            steps {
                sh '''
                   '''
            }
        }
    }
}
    