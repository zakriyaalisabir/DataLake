#	Make	targets	for	Mock DLA	Project

SHELL	:=	/bin/bash

APP:=	dla
REVISION:=$(shell	git	rev-parse	--short	HEAD)
SCHEMA:=	${APP}
MODE:=	development
VIRTUAL_ENV:=	venv
PYTHON_BIN:=	$(VIRTUAL_ENV)/bin

.PHONY:	setup	clean_build

init:
	cp	".env.sample"	".env"

install:
	pip	install	-r	requirements/${MODE}.txt

config:
	python	config.py

clean:
	rm	--force	--recursive	build/
	rm	--force	--recursive	dist/
	rm	--force	--recursive	*.egg-info

virtualenv.create:
	python3	-m	venv	$(VIRTUAL_ENV)
	@echo	'Virtual	Environment	for	DLA	is	created.'

virtualenv.activate:
	source	${PYTHON_BIN}/activate
	@echo	'Virtual	Environment	for	DLA	is	activated.'

virtualenv.deactivate:
	deactivate

virtualenv:virtualenv.create	virtualenv.activate

bootstrap:
	clean	init	virtualenv	install	config

cmd:
	python $(CMD) $(ARG)

all:bootstrap