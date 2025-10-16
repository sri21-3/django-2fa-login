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
        . venv/bin/activate
        
        pip install --upgrade pip
        pip install -r requirements.txt
        '''
      }
    }

    stage('Lint & Checks') {
      steps {
        sh '''
              source venv/bin/activate
              pip install flake8 black isort
              bin/flake8 .
              isort --check-only --profile black --line-length 88 . || true
              black --check --line-length 88 . || true
              SECRET_KEY=ci DEBUG=False ${PYTHON} manage.py check --deploy --fail-level WARNING || true
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


