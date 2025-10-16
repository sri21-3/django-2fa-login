pipeline {
  agent any

  options {
    ansiColor('xterm')
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    PYTHON = 'python3'
    DOCKER_IMAGE = '2fa-email-login:web'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh '''
        # check python version
        python3 -V
        
        # Create virtual environment in the workspace
        python3 -m venv venv
        
        # Activat the virtual environment
        source venv/bin/activate
        
        sh "python3 -m pip install --upgrade pip"
        sh "pip install -r requirements.txt"
        '''
      }
    }

    stage('Lint & Checks') {
      steps {
        sh "pip install flake8 black isort"
        sh "flake8 || true"
        sh "isort --check-only --profile black --line-length 88 . || true"
        sh "black --check --line-length 88 . || true"
        sh "SECRET_KEY=ci DEBUG=False ${PYTHON} manage.py check --deploy --fail-level WARNING || true"
      }
    }

    stage('Docker Build') {
      steps {
        sh 'docker version || true'
        sh "docker build -t ${DOCKER_IMAGE} ."
      }
    }

    stage('Archive') {
      steps {
        archiveArtifacts artifacts: 'Dockerfile, docker-compose.yml, Jenkinsfile, README.md, PRD.md', fingerprint: true
      }
    }
  }

  post {
    always {
      echo "Build finished: ${currentBuild.currentResult}"
    }
  }
}


