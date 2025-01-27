agent any

    environment {
        VIRTUAL_ENV = "${WORKSPACE}/venv"
        IMAGE_NAME = "flask-app:latest"
        SCAN_SCRIPT_URL = "https://raw.githubusercontent.com/MandarPhadke/Container-Image-Vulnerability-Scanner-with-Reporting/main/scripts/scan_docker_pods.py"
        SCAN_OUTPUT_FILE = "scan_results.json"
    }

    stages {
       {
                git branch: 'main', url: 'https://github.com/MandarPhadke/DevOps-Simulated-2FA-Flask.git'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Flask Application') {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }
        stage('Download and Scan Docker Image') {
            steps {
                sh './venv/bin/python app.py &'
                script {
                    sh """
                        curl -o scan_docker_pods.py ${SCAN_SCRIPT_URL}
                        python3 scan_docker_pods.py --podname ${IMAGE_NAME} --output ${SCAN_OUTPUT_FILE}
                    """
                    
                    def scanResults = readJSON(file: SCAN_OUTPUT_FILE)
                    def criticalCount = 0
                    for (result in scanResults.Results) {
                        for (vuln in result.Vulnerabilities) {
                            if (vuln.Severity == "CRITICAL") {
                                criticalCount++
                            }
                        }
                    }
                    if (criticalCount > 0) {
                        echo "Critical vulnerabilities found: ${criticalCount}"
                        error("Stopping build due to security vulnerabilities.")
                    } else {
                        echo "No critical vulnerabilities found."
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "${SCAN_OUTPUT_FILE}", fingerprint: true
                }
            }
        }
    stage('Deploy Flask App') {
    steps {
        sh 'docker build -t flask-app .'
        sh 'docker run -d -p 5001:5001 flask-app'
        stage('Deploy Flask Application') {
            steps {
                sh "docker run -d -p 5000:5000 ${IMAGE_NAME}"
            }
        }
    }
    }

    post {
        success {
            echo 'Build and deployment successful!'
            echo 'Build, scan, and deployment successful!'
        }
        failure {
            echo 'Build failed. Check logs for details.'
            echo 'Build or security scan failed!'
        }
    }
}
