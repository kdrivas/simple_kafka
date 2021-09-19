from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from kafka import KafkaProducer

import os
import time
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
messages = ['hola', 'mundo']

KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_SERVER', 'kafka')
KAFKA_CONN = KAFKA_SERVER + ":" + KAFKA_PORT

def on_send_success(r):
  print('success')

def on_send_error(excp):
  print('Error', exc_info=excp)

def get_kafka_conn_object(timeout=3000):
  for _ in range(timeout):
    time.sleep(3)
    try:
      return KafkaProducer(bootstrap_servers=KAFKA_CONN, 
                          value_serializer=lambda x: json.dups(x).encode('utf-8'),
                          retries=5)
    except:
      print('Waiting kafka producer')
  print('Timeout!!')

kafka_prod = get_kafka_conn_object()

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})

@app.post('/', response_class=HTMLResponse)
def submit_messages(request: Request, message: str=Form(...)):
  # test is the name of the topic
  kafka_prod.sent('test', json.dumps(str(message))).add_callback(on_send_success).add_errback(on_send_error)
  kafka_prod.flush()
  return templates.TemplateResponse("producer.html", {"request": request, "messages": messages})



