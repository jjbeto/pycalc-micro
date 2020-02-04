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
	rm --force --recursive build/     || true
	rm --force --recursive dist/      || true
	rm --force --recursive *.egg-info || true


########################################################################################################################
######## Build containers ##############################################################################################
########################################################################################################################
.PHONY: build

build: clean-build
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
	echo "y" | docker system prune

clean: remove system-prune


########################################################################################################################
######## Test (Unit and integration) ###################################################################################
## TODO good idea: https://github.com/anirbanroydas/ci-testing-python/blob/master/tests/unit/test_unit_identidock.py
########################################################################################################################
.PHONY: test test-unit test-integration

test-unit:
	bash -c "tests/test.sh evaluate unit        $(UNIT_TESTING_NAME) $(UNIT_TEST_DIR) $(PROJECT_ROOT_DIR)"

test-integration:
	bash -c "tests/test.sh evaluate integration $(INTEGRATION_TESTING_NAME) $(INTEGRATION_TEST_DIR) $(PROJECT_ROOT_DIR)"

test: system-prune test-unit test-integration


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
	@echo "    test-unit"
	@echo "        Perform Unit tests in Docker Container"
	@echo "    test-integration"
	@echo "        Perform Integration tests in Docker Container"
	@echo "    test"
	@echo "        Test Everything (unit and Integration)"
