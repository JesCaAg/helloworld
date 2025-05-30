
pipeline {
    agent any

    stages {
        stage('Jenkins1') {
            steps {
                deleteDir() // Eliminamos lo que hubiera en el workspace
                echo 'Primer echo' // 1er ejercicio de Jenkins 1, hacer un echo
                git branch: 'feature_fix_coverage', url: 'https://github.com/JesCaAg/helloworld.git' // 2o ejercicio de Jenkins 1, traer el repo de codigo
                bat 'dir' // 3o ejercicio de Jenkins 1, hacer un dir para verificar la descarga del repositorio
                echo WORKSPACE // 4o ejercicio de Jenkins 1, verificar el workspace
            }
        }
        
        stage('Pruebas') {
            parallel { // 3er ejecicio de Jenkins2, hacer paralelas las etapas de pruebas unitarias y de servicio
            // Añadidas posteriormente para el cp 1.2 pruebas de analisis de codigo estatico y seguridad    
                stage('Jenkins2 Unit'){ // 1er ejercicio de Jenkins2, crear una etapa con la ejecucion de pruebas unitarias
                    steps {
                        script {
                            catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                            // Como solo debemos ejecutar las pruebas unitarias una vez, vamos a ejecutar las pruebas e ir recolectando cobertura
                                def res_unit = bat (script: // Siempre se marcará en verde la etapa, sea cual sea el resultado de las pruebas
                                    '''
                                        set PYTHONPATH=.
                                        py -m coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=result-unit.xml test\\unit
                                    ''', returnStatus: true)
                                junit 'result-unit.xml'
                            }
                        }
                    }
                }
                
                stage('Jenkins2 Service'){ // 2o ejercicio de Jenkins2, crear una etapa con la ejecucion de pruebas de servicio
                    steps {
                        script{
                            catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                                bat'''
                                    set FLASK_APP=app\\api.py
                                    start py -m flask run
                                    start java -jar C:\\Users\\Jesus\\helloworld\\1.1\\wiremock-standalone-3.13.0.jar --port 9090 --root-dir test\\wiremock
                                '''
                                // Comprobamos que estan escuchando tanto flask como wiremock, si no, esperamos
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
                                
                                def res_service = bat (script: // Siempre se marcará en verde la etapa, sea cual sea el resultado de las pruebas
                                    '''
                                        set PYTHONPATH=.
                                        py -m pytest --junitxml=result-rest.xml test\\rest
                                    ''',returnStatus: true)
                                    
                                //Cerramos el proceso de flask, que es el que escucha en el puerto 5000
                                bat '''
                                	@echo off
                                	setlocal enabledelayedexpansion
                                	set "PIDS="
                                	for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
                                    	echo !PIDS! | find "%%a" >nul
                                    	if errorlevel 1 (
                                    		taskkill /F /PID %%a
                                    		set "PIDS=!PIDS! %%a"
                                    	)
                                	)
                                	endlocal
                            	'''
                            	//Cerramos el proceso de wiremock, que es el que escucha en el puerto 9090
                            	bat '''
                                	@echo off
                                	setlocal enabledelayedexpansion
                                	set "PIDS="
                                	for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9090 ^| findstr LISTENING') do (
                                    	echo !PIDS! | find "%%a" >nul
                                    	if errorlevel 1 (
                                    		taskkill /F /PID %%a
                                    		set "PIDS=!PIDS! %%a"
                                    	)
                                	)
                                	endlocal
                            	'''
                                junit 'result-rest.xml'
                            }
                        }
                    }
                }
                 
                stage('Static'){ // Creacion de la etapa con la ejecucion de pruebas de analisis de codigo estatico, usando flake8
                    steps {
                        catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                            bat 'py -m flake8 --format=pylint --exit-zero app >flake8.out'
                            recordIssues enabledForFailure: true, tools: [flake8(name: 'Flake8', pattern: 'flake8.out')],
                                qualityGates: [
                                    [threshold: 8, type: 'TOTAL', unstable: true],
                                    [threshold: 10, type: 'TOTAL', unstable: false]
                                ]
                        }
                    }
                }
                
                stage('Security test'){ // Creacion de la etapa con la ejecucion de pruebas de seguridad, usando bandit
                    steps {
                        catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                            bat 'py -m bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"'
                            recordIssues enabledForFailure: true, tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')],
                                qualityGates: [
                                    [threshold: 2, type: 'TOTAL', unstable: true],
                                    [threshold: 4, type: 'TOTAL', unstable: false]
                                ]
                        }
                    }
                }
            }
        }
        
        stage('Coverage'){ // Creacion de la etapa con la ejecucion del reporte de pruebas de cobertura, usando coverage, y pintado del reporte
            steps {
                catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                    // Solo tenemos que generar el fichero xml, porque los datos de cobertura los recogimos mientras hacíamos pruebas unitarias
                    bat '''
                        py -m coverage xml
                    '''
                    recordCoverage (enabledForFailure: true, tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']],
                        qualityGates: [
                            [metric: 'LINE', threshold: 85.0, criticality: 'FAILURE'],
                            [metric: 'LINE', threshold: 95.0, criticality: 'UNSTABLE'],
                            [metric: 'BRANCH', threshold: 80.0, criticality: 'FAILURE'],
                            [metric: 'BRANCH', threshold: 90.0, criticality: 'UNSTABLE']
                        ]
                    )
                }
            }
        }
        
        stage('Performance'){ // Creacion de la etapa con la ejecucion de pruebas de carga, usando jmeter
            steps {
                catchError(buildResult:'UNSTABLE', stageResult:'FAILURE') {
                    bat '''
                        set FLASK_APP=app\\api.py
                        start py -m flask run
                    '''
                    script {
                        def url_flask = 'http://127.0.0.1:5000'
                        def intento = 1
                        def intentos_max = 10
                        while ( intento <= intentos_max) {
                            try {
                                bat(script: "curl -s -o nul ${url_flask}")
                                intento = 11
                            }
                            catch (e) {
                                sleep(time: 10, unit: 'SECONDS')
                                intento++
                            }
                        }
                    }
                    bat 'C:\\Users\\Jesus\\helloworld\\apache-jmeter-5.6.3\\bin\\jmeter -n -t test\\jmeter\\flask.jmx -f -l flask.jtl'
                    perfReport sourceDataFiles: 'flask.jtl'
                    // Cerramos el proceso de flask, que es el que escucha en el puerto 5000
                    bat '''
                    	@echo off
                    	setlocal enabledelayedexpansion
                    	set "PIDS="
                    	for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
                        	echo !PIDS! | find "%%a" >nul
                        	if errorlevel 1 (
                        		taskkill /F /PID %%a
                        		set "PIDS=!PIDS! %%a"
                        	)
                    	)
                    	endlocal
                	'''
                }
            }
        }
    }
}
