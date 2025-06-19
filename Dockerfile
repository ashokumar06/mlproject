FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends awscli curl && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
