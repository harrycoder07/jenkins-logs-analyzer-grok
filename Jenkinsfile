pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat '''
                    echo Build started
                    dir || echo ERROR: Simulated failure
                    echo Build ended
                '''
            }
        }
        stage('Extract Logs') {
            steps {
                script {
                    def log = currentBuild.rawBuild.getLog(1000).join('\n')
                    writeFile file: 'logs/build_log.txt', text: log
                }
            }
        }
        stage('Analyze Logs with Grok') {
            steps {
                bat '''
                    python analyze_logs.py
                '''
            }
        }
        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'logs/build_log.txt, summaries/failure_summary.txt', allowEmptyArchive: true
            }
        }
    }
    post {
        failure {
            echo "Build failed. Check failure_summary.txt for Grok’s analysis."
        }
        always {
            echo "Pipeline completed."
        }
    }
}