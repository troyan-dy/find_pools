PYTHON ?= python3.15

setup:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r resuirements.dev.txt
test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m mypy app/
	$(PYTHON) -m flake8 app/ tests/

format:
	$(PYTHON) -m black app/ tests/
	$(PYTHON) -m isort app/ tests/

start:
	docker-compose up -d --build  && docker-compose logs -f
stop:
	docker-compose down
