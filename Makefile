#	Make	targets	for	Mock	DataLake	Project

SHELL	:=	/bin/bash

APP:=	datalake_rest_apis
CF_STACK_NAME:=	cf-mock-datalake-stack
REVISION:=$(shell	git	rev-parse	--short	HEAD)
SCHEMA:=	${APP}
SERVER:=	django_server
MODE:=	development
VIRTUAL_ENV:=	venv
MSG:=	updated code
ORIGIN:=	dev

.PHONY:	init	clean

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
	rm	--force	--recursive	src_handlers/temp/*

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
	python3 src_handlers/troposphere/index.py

cf.push_stack:
	aws	configure
	aws cloudformation	create-stack	--stack-name	${CF_STACK_NAME}	--template-body	file://src_handlers/temp/cf_stack.yaml	--capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

cf.update_stack:cf.create_stack
	aws	configure
	aws cloudformation	update-stack	--stack-name	${CF_STACK_NAME}	--template-body	file://src_handlers/temp/cf_stack.yaml	--capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

cf.delete_stack:
	aws	cloudformation	delete-stack	--stack-name	${CF_STACK_NAME}

cf:cf.create_stack cf.push_stack

migrate:
	python3	manage.py	makemigrations
	python3	manage.py	migrate

migrate.undo_all:
	python3	manage.py	migrate	${APP}	zero

app.create:
	python3	manage.py	startapp	${APP}

server.create:
	django-admin startproject ${SERVER} .

server.run:
	python3	manage.py	runserver

django.create.su:
	python3 manage.py createsuperuser

django:server.create app.create#only for creating a django server and django app for REST apis 

git_sync_dev:
	git	fetch --all
	git	pull	origin ${ORIGIN}
	git	add	.
	git	commit	-m	"${MSG}"
	git	push	origin	${ORIGIN} 

bootstrap:init	virtualenv	install

all:bootstrap	server.run