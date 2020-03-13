#	Make	targets	for	Mock	DataLake	Project

SHELL	:=	/bin/bash

APP:=	datalake
REVISION:=$(shell	git	rev-parse	--short	HEAD)
SCHEMA:=	${APP}
SERVER:=	django_server
MODE:=	development
VIRTUAL_ENV:=	venv

.PHONY:	setup	clean_build	bootstrap

init:
	cp	".env.sample"	".env"

install:
	pip3	install	-r	requirements/${MODE}.txt

config:
	python3	config.py

clean:
	rm	--force	--recursive	build/
	rm	--force	--recursive	dist/
	rm	--force	--recursive	*.egg-info
	rm	--force	--recursive	src/temp/*

virtualenv.create:
	python3	-m	venv	$(VIRTUAL_ENV)
	@echo	'Virtual	Environment	for	${APP}	is	created.'

virtualenv.activate:
	source	${VIRTUAL_ENV}/bin/activate
	@echo	'Virtual	Environment	for	${APP}	is	activated.'

virtualenv.deactivate:
	deactivate

virtualenv:virtualenv.create	virtualenv.activate

cf.create_stack:
	python3 src/index.py

cf.push_stack:
	aws cloudformation create-stack --stack-name learncf-subnet --template-body file://src/temp/cf_stack.yaml

cf:cf.create_stack cf.push_stack

migrate:
	python	manage.py	migrate

migrate.undo_all:
	python	manage.py	migrate	${APP}	zero

app.create:
	python	manage.py	startapp	${APP}

server.create:
	django-admin startproject ${SERVER} .

server.run:migrate
	python	manage.py	runserver

run:server.run

bootstrap:clean	init	virtualenv	install	config server.create app.create

all:bootstrap	run	#cf