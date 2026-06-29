pipeline {
    agent none

    environment {
        IMAGE_NAME = "devsecops-demo"
        REGISTRY   = "ghcr.io/roma-rgb-tech"
    }

    stages {

        stage('Lint & Test') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh '''#!/bin/bash
                    set -euo pipefail
                    pip install --no-cache-dir --upgrade pip
                    pip install --no-cache-dir ruff pytest -r requirements.txt
                    ruff check app/
                    pytest tests/ -v
                '''
            }
        }

        stage('Security Scan') {
            agent {
                docker {
                    image 'docker:cli'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''#!/bin/sh
                    set -eu
                    docker run --rm -v "$(pwd):/repo" aquasec/trivy:latest fs \
                        --severity CRITICAL,HIGH --exit-code 1 /repo
                '''
            }
        }

        stage('Build & Push') {
            agent {
                docker {
                    image 'docker:cli'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'ghcr-token', variable: 'GHCR_TOKEN')]) {
                        sh '''#!/bin/sh
                            set -eu
                            echo "$GHCR_TOKEN" | docker login ghcr.io -u roma-rgb-tech --password-stdin
                        '''
                    }

                    sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."

                    if (env.BRANCH_NAME == 'main') {
                        sh "docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    } else {
                        echo "Push skiped: BRANCH_NAME='${env.BRANCH_NAME}', not 'main'."
                    }
                }
            }
            post {
                always {
                    sh 'docker logout ghcr.io || true'
                }
            }
        }
    }
}