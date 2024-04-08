
run:
	docker compose up --build

develop:
	docker compose exec developing /bin/bash

call_server:
	python developing/call_server/main.py

pull_llava:
	PYTHONPATH=. python developing/pull_llava/main.py

understand_image:
	PYTHONPATH=. python developing/understand_image/understand_image.py $(filter-out $@,$(MAKECMDGOALS))

%:
	@true
