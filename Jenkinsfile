pipeline {
    agent any

    stages {
        stage('Jenkins1') {
            steps {
                deleteDir() // Eliminamos lo que hubiera en el workspace
                echo 'Primer echo' // 1er ejercicio de Jenkins 1, hacer un echo
                git branch: 'feature_fix_racecond', url: 'https://github.com/JesCaAg/helloworld.git' // 2o ejercicio de Jenkins 1, traer el repo de codigo
                bat 'dir' // 3o ejercicio de Jenkins 1, hacer un dir para verificar la descarga del repositorio
                echo WORKSPACE // 4o ejercicio de Jenkins 1, verificar el workspace
            }
        }
        
        stage('Jenkins1 Build'){ // 5o ejercicio de Jenkins1, crear una etapa build (no necesaria por ser python)
            steps {
                echo 'Estoy construyendo' 
            }
        }
        
        stage('Pruebas') {
            parallel { // 3er ejecicio de Jenkins2, hacer paralelas las etapas de pruebas unitarias y de servicio   
                stage('Jenkins2 Unit'){ // 1er ejercicio de Jenkins2, crear una etapa con la ejecucion de pruebas unitarias
                    steps {
                        bat '''
                            set PYTHONPATH=.
                            py -m pytest --junitxml=result-unit.xml test\\unit
                        '''
                    }
                }
                
                 stage('Jenkins2 Service'){ // 2o ejercicio de Jenkins2, crear una etapa con la ejecución de pruebas de servicio
                    steps {
                        catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                           bat '''
                                curl -sO https://repo1.maven.org/maven2/org/wiremock/wiremock-standalone/3.13.0/wiremock-standalone-3.13.0.jar
                                set FLASK_APP=app\\api.py
                                start py -m flask run
                                start java -jar wiremock-standalone-3.13.0.jar --port 9090 --root-dir test\\wiremock  
                            '''
                            script {
                                def url_flask = 'http://127.0.0.1:5000'
                                def url_wiremock = 'http://127.0.0.1:9090'
                                def intento = 1
                                def intentos_max = 10
                                while ( intento <= intentos_max) {
                                    try {
                                        bat(script: "curl -s -o nul ${url_flask}")
                                        bat(script: "curl -s -o nul ${url_wiremock}")
                                        intento = 11
                                    }
                                    catch (e) {
                                        sleep(time: 10, unit: 'SECONDS')
                                        intento++
                                    }
                                }
                            }
                            bat '''
                                set PYTHONPATH=.
                                py -m pytest --junitxml=result-rest.xml test\\rest
                            '''
                        }
                    }
                 }
            }
        }
        
        stage ('Resultados') { // 3er ejercicio de Jenkins2, crear una última etapa para conectar con JUnit
            steps {
                junit 'result-*.xml'
            }
        }
    }
}
