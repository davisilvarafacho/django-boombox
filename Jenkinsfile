pipeline {
    agent any

    stages {
        stage ('Build') {
            steps {
                script {
                    dockerapp = docker.build("davisilvarafacho/django-boombox:${env.BUILD_ID}", '-f ./docker/Dockerfile ./')
                }
            }
        }

        stage ('Push Image') {
            steps {
                script {
                    docker.withRegistry("https://registry.hub.docker.com", 'dockerhub') {
                        dockerapp.push('latest')
                        dockerapp.push('${env.BUILD_ID}')
                    }
                }
            }
        }
    }   
}
