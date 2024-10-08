clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint-api:
	uvx ruff check --fix
	uvx djhtml .

lint-frontend:
	cd frontend && npm run lint

lint:
	@make lint-api
	@make lint-frontend

update:
	uv lock --upgrade
	uv sync

test-api:
	uv run python manage.py test

test-accounts:
	uv run python manage.py test accounts

test-profiles:
	uv run python manage.py test profiles

test-social:
	uv run python manage.py test social

test:
	@make test-api

check-api:
	uv run python manage.py check
	uv run phython manage.py check --deploy
	uv run python manage.py check --tag security

collect:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

run-api:
	uv run python manage.py runserver

run-front:
	cd frontend && npm run dev
