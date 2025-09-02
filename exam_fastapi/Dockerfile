FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ../requirements.txt .
COPY ../cassandra_orm .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "dev", "app.py"]