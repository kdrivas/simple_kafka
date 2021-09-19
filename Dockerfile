FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=0
WORKDIR /app
COPY requeriements.txt .
RUN pip install -r requeriements.txt
COPY . .
CMD cd app && uvicorn app:app --host 0.0.0.0