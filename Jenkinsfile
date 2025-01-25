pipeline {
    agent any

    environment {
        VIRTUAL_ENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/your-flask-repo.git'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh './venv/bin/python -m unittest discover tests'
            }
        }
        stage('Run Flask Application') {
            steps {
                sh './venv/bin/python app.py &'
            }
        }
    }
    stage('Deploy Flask App') {
    steps {
        sh 'docker build -t flask-app .'
        sh 'docker run -d -p 5000:5000 flask-app'
        }
    }

    post {
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build failed. Check logs for details.'
        }
    }
}
