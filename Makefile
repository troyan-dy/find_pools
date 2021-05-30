setup:
	pip3.9 install -r requirements.txt
	pip3.9 install -r resuirements.dev.txt
test:
	python3.9 -m pytest tests/

lint:
	python3.9 -m mypy app/
	python3.9 -m flake8 app/ tests/

format:
	python3.9 -m black app/ tests/
	python3.9 -m isort app/ tests/

start:
	docker-compose up -d --build  && docker-compose logs -f
stop:
	docker-compose down
