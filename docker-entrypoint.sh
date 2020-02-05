#!/bin/sh
set -e

if [ "$ENV" = "DEV" ]; then
	echo "Running Development Application"
	export FLASK_ENV=development
  python $MICROSERVICE/main.py

elif [ "$ENV" = "PROD" ]; then
	echo "Running Production Application"
	python $MICROSERVICE/main.py

else
	echo "Please provide an environment"
	echo "Stopping"
fi
