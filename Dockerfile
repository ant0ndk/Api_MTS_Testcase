FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
# RUN python mts_task/manage.py migrate

CMD ["python", "mts_task/manage.py", "runserver", "0.0.0.0:8000"]