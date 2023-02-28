run:
	python3 -m uvicorn api.main:app --reload --port 8888

migrate:
	python3 -m api.migrate_db


# tests
test:
	docker compose exec app python3.10 -m pytest -svv

re:
	docker compose exec app python3.10 -m pytest -svv --lf


# preformance
measure:
	docker compose exec app python3.10 -m pytest --durations=0

cov:
	docker compose exec app python3.10 -m pytest --cov --cov-report=html

report:
	google-chrome ./backend/htmlcov/index.html

profile:
	docker compose exec app python3.10 -m pytest --profile-svg
