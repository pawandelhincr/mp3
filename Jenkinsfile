pipeline {
    agent any

    stages {
        stage('Source') {
            steps {
                echo 'Fetching code from Git...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Compiling code...'
                // For example: sh './build.sh' or sh 'mvn compile'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // For example: sh './test.sh'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying to AWS...'
                // Add your deployment commands here
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
