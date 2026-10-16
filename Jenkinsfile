pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment { IMAGE_NAME = 'student-management' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Python setup') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }
        stage('Tests') {
            steps { sh '. .venv/bin/activate && pytest -q --junitxml=pytest-report.xml' }
            post { always { junit allowEmptyResults: true, testResults: 'pytest-report.xml' } }
        }
        stage('Docker build') {
            when { expression { fileExists('Dockerfile') } }
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .' }
        }
    }
    post {
        success { echo 'CI pipeline passed: tests successful and image build completed.' }
        failure { echo 'CI pipeline failed. Review the stage logs and test report.' }
        always { cleanWs(deleteDirs: true, notFailBuild: true) }
    }
}
