install:
	poetry install

migrate:
	poetry run python3 manage.py migrate

collectstatic:
	poetry run python3 manage.py collectstatic

build: install migrate collectstatic

run-server:
	poetry run python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

dev:
	poetry run python3 manage.py runserver

lint:
	poetry run flake8

test:
	poetry run python3 manage.py test

test-cov:
	poetry run coverage run manage.py test
	poetry run coverage xml

dev-cov:
	poetry run coverage run manage.py test
	poetry run coverage report -m

makemessages:
	poetry run python3 manage.py makemessages -a

compilemessages:
	poetry run python3 manage.py compilemessages
