FROM python:3.11-slim

# Cài đặt các dependencies cần thiết
#RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project vào container
COPY . .

EXPOSE 8011

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD uvicorn --app-dir src main:app --host 0.0.0.0 --port 8010
CMD ["make", "run"]

#docker build -t mockupartwork .