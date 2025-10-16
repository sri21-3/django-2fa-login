pipeline {
  agent any

  options {
    ansiColor('xterm')
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  environment {
    PYTHON = './venv/bin/python'
    PIP = './venv/bin/pip'
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
          python3 -V
          python3 -m venv venv
          ./venv/bin/pip install --upgrade pip
          ./venv/bin/pip install -r requirements.txt
        '''
      }
    }

    stage('Lint & Checks') {
      steps {
        sh '''
          ./venv/bin/pip install flake8 black isort

          echo "Running flake8..."
          ./venv/bin/flake8 .

          echo "Running isort..."
          ./venv/bin/isort --check-only --profile black --line-length 88 . || true

          echo "Running black..."
          ./venv/bin/black --check --line-length 88 . || true

          echo "Running Django system checks..."
          SECRET_KEY=ci DEBUG=False ./venv/bin/python manage.py check --deploy --fail-level WARNING || true
        '''
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

