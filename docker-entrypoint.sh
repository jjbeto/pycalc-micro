#!/bin/sh
set -e

if [ "$ENV" = "DEV" ]; then
	echo "Running Development Application"
# needs to configure setup.py
#	pip install --no-deps -e .
	python /service/app/main.py

elif [ "$ENV" = "UNIT_TEST" ]; then
	echo "Running Unit Tests"
# needs to configure setup.py
#	pip install --no-deps -e .
	exec pytest -v -s --cov=./ci_testing_python tests/unit

elif [ "$ENV" = "INTEGRATION_TEST" ]; then
	echo "Running Integration Tests"
# needs to configure setup.py
#	pip install --no-deps -e .
	exec pytest -v -s --cov=./ci_testing_python tests/integration

elif [ "$ENV" = "PROD" ]; then
	echo "Running Production Application"
# needs to configure setup.py
#	pip install --no-deps .
	python /service/app/main.py

else
	echo "Please provide an environment"
	echo "Stopping"
fi
