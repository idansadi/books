pipeline {
    agent {
        kubernetes {
            label 'ez-joy-friends'
            idleMinutes 5
            yamlFile '../../build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }
    environment {
        TAG = 'latest'
        MONGO_URI = 'mongodb://mongodb:27017/books'
        DOCKER_REGISTRY = 'docker.io' // Docker Hub registry URL
        DOCKER_IMAGE = 'idansadi/books' // Docker image name
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${TAG}")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml build'
                    sh 'docker-compose -f docker-compose.yaml up -d'
                    sh 'docker-compose -f docker-compose.yaml run test pytest'
                    sh 'docker-compose -f docker-compose.yaml down'
                }
            }
        }

        stage('Create Pull Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    def headBranch = env.BRANCH_NAME
                    def baseBranch = 'main'

                    // Extracting title and description from the latest commit message
                    def latestCommitMessage = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                    def title = latestCommitMessage.split('\n')[0]
                    def body = latestCommitMessage - title

                    def authToken = env.GITHUB_TOKEN
                    def owner = 'your-username'
                    def repo = 'your-repo'

                    def apiUrl = "https://api.github.com/repos/${owner}/${repo}/pulls"

                    def payload = """
                    {
                        "title": "${title}",
                        "body": "${body}",
                        "head": "${headBranch}",
                        "base": "${baseBranch}"
                    }
                    """

                    sh "curl -X POST -H 'Authorization: token ${authToken}' -d '${payload}' ${apiUrl}"
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${TAG}").push()
                    }
                }
            }
        }
    }
}
