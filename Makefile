
ENV_FILE := .env
-include ${ENV_FILE}

install-requirements:
	@	pip install -r requirements.txt

run-behave:
	@	behave tests

start-fuseki:
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/fuseki/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-fuseki:
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/fuseki/docker-compose.yml --env-file ${ENV_FILE} down


start-graphdb:
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/graphdb/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-graphdb:
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/graphdb/docker-compose.yml --env-file ${ENV_FILE} down