########################################################################################################################
######## Clean  up #####################################################################################################
########################################################################################################################
.PHONY: clean-pyc clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~'    -exec rm --force {} +
	find . | grep -E '(__pycache__)' | xargs rm -rf

clean-build:
	@echo "🧹 Cleaning old build"
	rm --force --recursive build/     || true
	rm --force --recursive dist/      || true
	rm --force --recursive *.egg-info || true


########################################################################################################################
######## Build containers ##############################################################################################
########################################################################################################################
.PHONY: build

build: clean-build
	@echo "🔨 Building images"
	docker-compose build


########################################################################################################################
######## Start containers ##############################################################################################
########################################################################################################################
.PHONY: start

start: build
	docker-compose up -d


########################################################################################################################
######## Stop and remove containers ####################################################################################
########################################################################################################################
.PHONY: stop

stop:
	docker-compose down -v


########################################################################################################################
######## Check logs ####################################################################################################
########################################################################################################################
.PHONY: logs logs-evaluate

logs:
	docker-compose logs --follow --tail=10

logs-evaluate:
	docker-compose logs --follow --tail=10 pycalc-evaluate


########################################################################################################################
######## Cleanup docker env ############################################################################################
########################################################################################################################
.PHONY: system-prune clean

system-prune:
	@echo "🛎 System prune"
	echo "y" | docker system prune

clean: stop system-prune


########################################################################################################################
######## Test (Unit and integration) ###################################################################################
## TODO good idea: https://github.com/anirbanroydas/ci-testing-python/blob/master/tests/unit/test_unit_identidock.py
########################################################################################################################
.PHONY: test unit-test test-integration

unit-test:
	@echo "🍜 Running unit-tests"
	docker build -t jjbeto/pycalc-micro-unit-test -f Dockerfile.test .

integration-test: start
	@echo "🍜 Running integration-tests"
	@echo "🍜 testing service 'evaluate'"
	cd tests/integration && chmod +x test_evaluate.sh && ./test_evaluate.sh -u http://localhost:5000


test: unit-test integration-test


########################################################################################################################
######## Help ##########################################################################################################
########################################################################################################################
.PHONY: help

help:
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    build"
	@echo "        Build Project in Docker Container"
	@echo "    start"
	@echo "        Build and Run Project in Docker Container"
	@echo "    stop"
	@echo "        Stop and Remove Docker Container"
	@echo "    logs"
	@echo "        Alias for check-logs-dev"
	@echo "    logs-evaluate"
	@echo "        Check logs of Docker Container jjbeto/pycalc-micro-evaluate"
	@echo "    clean"
	@echo "        Clean the Docker Container Env"
	@echo "    system-prune"
	@echo "        Clean Environment: Docker Containers, volumes, images which are dangling"
	@echo "    unit-test"
	@echo "        Perform Unit tests in Docker Container"
	@echo "    integration-test"
	@echo "        Perform Integration tests in Docker Container"
	@echo "    test"
	@echo "        Test Everything (unit and Integration)"
