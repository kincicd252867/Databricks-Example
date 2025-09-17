pipeline {
    agent any
    environment {
        // Project configuration
        PROJECT_NAME = 'Databricks-Example'
        PROJECT_VERSION = "1.0.0.${env.BUILD_NUMBER}"
        
        // Python configuration
        PYTHON_VERSION = '3.10'
        VENV_DIR = "${env.WORKSPACE}/venv"
        
        // SonarQube configuration
        SONAR_SCANNER_HOME = tool 'SonarQubeScanner'
        
        // Artifact paths
        WHEEL_NAME = "my_project-${PROJECT_VERSION}-py3-none-any.whl"
        WHEEL_PATH = "${env.WORKSPACE}/dist/${WHEEL_NAME}"
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    // Get the current Git commit hash for tracking
                    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh """
                    chmod +x scripts/setup_environment.sh
                    scripts/setup_environment.sh ${PYTHON_VERSION} ${VENV_DIR}
                """
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                sh """
                    source ${VENV_DIR}/bin/activate
                    pip install -r requirements-dev.txt
                    python -m pytest tests/unit/ -v --cov=src --cov-report=xml:coverage.xml
                """
            }
            post {
                always {
                    junit '**/test-reports/*.xml'  // Capture test results
                    archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube-Server') {
                    sh """
                        source ${VENV_DIR}/bin/activate
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${PROJECT_NAME} \
                        -Dsonar.projectName=${PROJECT_NAME} \
                        -Dsonar.projectVersion=${PROJECT_VERSION} \
                        -Dsonar.sources=src,notebooks \
                        -Dsonar.tests=tests/unit \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.exclusions=**/__init__.py,**/test_*.py \
                        -Dsonar.test.inclusions=**/test_*.py \
                        -Dsonar.gitlab.project_id=${PROJECT_NAME} \
                        -Dsonar.gitlab.commit_sha=${env.GIT_COMMIT} \
                        -Dsonar.gitlab.ref_name=${env.BRANCH_NAME}
                    """
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build Package') {
            steps {
                sh """
                    source ${VENV_DIR}/bin/activate
                    python setup.py bdist_wheel
                """
                archiveArtifacts artifacts: "dist/${WHEEL_NAME}", fingerprint: true
            }
        }
        
        stage('Deploy to Dev') {
            environment {
                DATABRICKS_HOST = credentials('databricks-dev-host')
                DATABRICKS_TOKEN = credentials('databricks-dev-token')
            }
            steps {
                sh """
                    chmod +x scripts/deploy_to_databricks.sh
                    scripts/deploy_to_databricks.sh \
                        ${DATABRICKS_HOST} \
                        ${DATABRICKS_TOKEN} \
                        ${WHEEL_PATH} \
                        ${PROJECT_VERSION} \
                        dev
                """
            }
        }
        
        stage('Run Integration Tests') {
            environment {
                DATABRICKS_HOST = credentials('databricks-dev-host')
                DATABRICKS_TOKEN = credentials('databricks-dev-token')
            }
            steps {
                sh """
                    chmod +x scripts/run_integration_tests.sh
                    scripts/run_integration_tests.sh \
                        ${DATABRICKS_HOST} \
                        ${DATABRICKS_TOKEN} \
                        ${VENV_DIR}
                """
            }
        }
        
        stage('Deploy to Prod') {
            environment {
                DATABRICKS_HOST = credentials('databricks-prod-host')
                DATABRICKS_TOKEN = credentials('databricks-prod-token')
            }
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    input message: 'Deploy to production?', ok: 'Deploy'
                }
                sh """
                    chmod +x scripts/deploy_to_databricks.sh
                    scripts/deploy_to_databricks.sh \
                        ${DATABRICKS_HOST} \
                        ${DATABRICKS_TOKEN} \
                        ${WHEEL_PATH} \
                        ${PROJECT_VERSION} \
                        prod
                """
            }
        }
    }
    post {
        always {
            sh """
                # Clean up virtual environment
                rm -rf ${VENV_DIR} || true
                
                # Clean up build artifacts
                rm -rf build/ dist/ *.egg-info/ || true
                
                # Clean up coverage reports
                rm -f coverage.xml || true
            """
            cleanWs()
        }
        success {
            echo "Pipeline ${PROJECT_NAME} ${PROJECT_VERSION} completed successfully!"
            // Optional: Send success notification
        }
        failure {
            echo "Pipeline ${PROJECT_NAME} ${PROJECT_VERSION} failed!"
            // Optional: Send failure notification
        }
        unstable {
            echo "Pipeline ${PROJECT_NAME} ${PROJECT_VERSION} is unstable!"
            // Optional: Send unstable notification
        }
    }
}
