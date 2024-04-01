
run:
	docker compose up --build

develop:
	docker compose exec developing /bin/bash

call_server:
	python developing/call_server/main.py

clone:
	git clone git@github.com:agcooke/ai-programing.git
