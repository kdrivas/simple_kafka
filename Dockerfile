FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=0
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD uvicorn app:app --host 0.0.0.0