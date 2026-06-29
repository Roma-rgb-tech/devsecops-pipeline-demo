pipeline {
    agent {
        docker {
            image 'python:3.11-slim' 
            args '-u root'
        }
    }

    environment {
        IMAGE_NAME = "devsecops-demo"
        REGISTRY   = "ghcr.io/roma-rgb-tech"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh 'pip install ruff && ruff check app/'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }

      stage('Security Scan') {
       steps {
        sh '''
            wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
            echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list
            apt-get update && apt-get install trivy -y
            
            trivy fs . --severity CRITICAL,HIGH --exit-code 1
        '''
    }
}

        stage('Build') {
            steps {
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Push') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([string(credentialsId: 'ghcr-token', variable: 'GHCR_TOKEN')]) {
                    sh '''
                        echo $GHCR_TOKEN | docker login ghcr.io -u roma-rgb-tech --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}