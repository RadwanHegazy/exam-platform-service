FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY reqirements.txt .
RUN pip install --no-cache-dir -r reqirements.txt

COPY . .

CMD ["fastapi", "dev", "app.py"]