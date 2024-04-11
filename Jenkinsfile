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
        DOCKER_IMAGE = 'idansadi/books' // Docker image name
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Configure Git') {
            steps {
                script {
                    sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/books_dev'
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG} ."
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
                    def title
                    def body

                    // Extracting title and description from the latest commit message
                    def latestCommitMessage = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                    def messageLines = latestCommitMessage.split('\n')
                    title = messageLines[0]
                    if (messageLines.size() > 1) {
                        body = messageLines.tail().join('\n')
                    } else {
                        body = ''  // If there's no body, set it to an empty string
                    }
                    
                    def owner = 'idansadi'
                    def repo = 'books'
                    def apiUrl = "https://api.github.com/repos/${owner}/${repo}/pulls"
                    def payload = """
                    {
                        "title": "${title}",
                        "body": "${body}",
                        "head": "${headBranch}",
                        "base": "${baseBranch}"
                    }
                    """

                    sh """
                    curl -X POST -H 'Authorization: token ${env.GITHUB_TOKEN}' \\
                    -d '${payload}' ${apiUrl}
                    """
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
                    sh "docker push ${DOCKER_IMAGE}:${TAG}"
                }
            }
        }
    }
}
