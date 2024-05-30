ENV_FILE := .env
-include ${ENV_FILE}

install:
	@ pip install -r requirements.txt

run-behave:
	@ behave tests

start-fluree:
	@ docker-compose -p ${DOCKER_PROJECT} --file ./infra/fluree_server/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-fluree:
	@ docker-compose -p ${DOCKER_PROJECT} --file ./infra/fluree_server/docker-compose.yml --env-file ${ENV_FILE} down