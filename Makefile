clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	uvx ruff check --fix
	uvx djhtml .

update:
	uv lock --upgrade
	uv sync

test:
	uv run python manage.py test

test-accounts:
	uv run python manage.py test accounts

test-profiles:
	uv run python manage.py test profiles

check:
	uv run python manage.py check
	uv run phython manage.py check --deploy
	uv run python manage.py check --tag security

collect:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver
