#!/bin/sh
set -e

if [ "$ENV" = "DEV" ]; then
	echo "Running Development Application"
	export FLASK_ENV=development
  python $MICROSERVICE/main.py

elif [ "$ENV" = "UNIT_TEST" ]; then
	echo "Running Unit Tests"
	exec pytest -v -s --cov=./tests tests/unit

elif [ "$ENV" = "INTEGRATION_TEST" ]; then
	echo "Running Integration Tests"
	exec pytest -v -s --cov=./tests tests/integration

elif [ "$ENV" = "PROD" ]; then
	echo "Running Production Application"
	python $MICROSERVICE/main.py

else
	echo "Please provide an environment"
	echo "Stopping"
fi
