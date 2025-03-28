MAIN_PATH=src.main
# APP_HOST=0.0.0.0
# APP_PORT=8011

# # Sử dụng Bash shell
# SHELL := /bin/bash

# # Lệnh kích hoạt Conda shell hook
# CONDA_HOOK = eval "$$(conda shell.bash hook)"

# deConda:
# 	$(CONDA_HOOK) && conda deactivate
# actConda:
# 	$(CONDA_HOOK) && conda activate fastapi

ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

install:
	pip install -r requirements.txt

resetDbMock:
	rm test.db || true & touch test.db

genEnv:
	cp ./sample.env .env

migrateGen:
	alembic revision --autogenerate -m "Migration message"
migrateUp:
	alembic upgrade head
migrateDown:
	alembic downgrade -1

printEnv:
	printenv | grep '^APP'
	printenv | grep '^DB_'

dev:
	uvicorn $(MAIN_PATH):app --host $(APP_HOST) --port $(APP_PORT) --reload
runNew:
	python src/main.py
run:
	uvicorn $(MAIN_PATH):app --host $(APP_HOST) --port $(APP_PORT)
# uvicorn --app-dir src $(MAIN_PATH):app --host $(APP_HOST) --port $(APP_PORT) --reload
# uvicorn --app-dir src main:app --host 0.0.0.0 --port 8010 --reload

# Kiểm tra format code với black
format:
	black .

# Kiểm tra lỗi với flake8
lint:
	flake8 .

# Chạy các test case
test:
	pytest

# Build lại môi trường (cài lại thư viện)
rebuild:
	pip install --upgrade pip
	pip install -r requirements.txt

# Clean các file không cần thiết
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +