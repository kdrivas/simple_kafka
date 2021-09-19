from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from kafka import KafkaProducer

import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
messages = ['hola', 'mundo']

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_SERVER', 'kafka')
KAFKA_CONN = KAFKA_SERVER + ":" + KAFKA_PORT

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})

@app.post('/', response_class=HTMLResponse)
def submitMessage(request: Request, message: str=Form(...)):
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})



