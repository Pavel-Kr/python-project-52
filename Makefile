install:
	poetry install

dev:
	poetry run python3 manage.py runserver

create-dev-db:
	createdb task_manager_db