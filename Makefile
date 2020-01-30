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
	bash -c "source docker.env && docker-compose -p $(DOCKER_REPO) build"


########################################################################################################################
######## Start containers ##############################################################################################
########################################################################################################################
.PHONY: start

start: build
	bash -c "source docker.env && docker-compose -p $(DOCKER_REPO) up -d"


########################################################################################################################
######## Stop running containers #######################################################################################
########################################################################################################################
.PHONY: stop

stop:
	docker-compose -p $(DOCKER_REPO) stop


########################################################################################################################
######## Stop and remove containers ####################################################################################
########################################################################################################################
.PHONY: remove

remove: stop
	docker-compose -p $(DOCKER_REPO) rm --force -v


########################################################################################################################
######## Check logs ####################################################################################################
########################################################################################################################
.PHONY: check-logs check-logs-evaluate

check-logs:
	docker-compose -p $(DOCKER_REPO) logs --follow --tail=10

check-logs-evaluate:
	docker-compose -p $(DOCKER_REPO) logs --follow --tail=10 pycalc-evaluate


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
.PHONY: test test-unit test-component test-contract test-integration test-e2e test-system test-ui-acceptance test-functional

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
	@echo "        Build Project Docker Container"
	@echo "    start"
	@echo "        Start and Run Project in Docker Container"
	@echo "    stop"
	@echo "        Stop Docker Container"
	@echo "    remove"
	@echo "        Remove Docker Container"
	@echo "    check-logs"
	@echo "        Alias for check-logs-dev"
	@echo "    check-logs-evaluate"
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
