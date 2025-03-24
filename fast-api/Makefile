MAIN_PATH=src.main
HOST=0.0.0.0
PORT=8010
# Sử dụng Bash shell
SHELL := /bin/bash

# Lệnh kích hoạt Conda shell hook
CONDA_HOOK = eval "$$(conda shell.bash hook)"

deConda:
	$(CONDA_HOOK) && conda deactivate
actConda:
	$(CONDA_HOOK) && conda activate fastapi

resetDbMock:
	rm test.db || true & touch test.db

genEnv:
	cp ./sample.env .env

install:
	pip install -r requirements.txt

migrateGen:
	alembic revision --autogenerate -m "Migration message"
migrateUp:
	alembic upgrade head
migrateDown:
	alembic downgrade -1

# dev:
# 	fastapi dev ./src/main.py

# Chạy ứng dụng FastAPI
run:
	uvicorn $(MAIN_PATH):app --host $(HOST) --port $(PORT) --reload
# uvicorn --app-dir src $(MAIN_PATH):app --host $(HOST) --port $(PORT) --reload
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
# run:
# 	@. .venv/bin/activate && python3 src/main.py

# api:
# 	@. .venv/bin/activate && uvicorn --app-dir src api:app --port 9090 --reload