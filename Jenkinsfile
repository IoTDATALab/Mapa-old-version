pipeline {
    agent any

    environment {
        NameSpace='linwenjun'
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {

        stage('checkout') {
            steps {
                git poll: true, url: 'https://github.com/linwenjun/express-demo.git', branch: 'master'
            }
        }

        stage('standard') {
            steps {
                bat 'echo test'
            }
        }

        stage('test') {
            steps {
                bat 'echo test'
            }
        }

        stage('install dependencies') {
            steps {
                bat 'echo install'
            }
        }

        stage('deploy') {
            steps {
                bat 'echo deploy'
            }
        }
    }
}