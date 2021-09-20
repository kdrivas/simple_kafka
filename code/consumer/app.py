from kafka import KafkaConsumer
import requests
import os
import time
import json

KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PORT = os.getenv('KAFKA_PORT')
KAFKA_CONN = KAFKA_SERVER + ':' + KAFKA_PORT
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
PRODUCER_ENDPOINT = os.getenv('PRODUCER_ENDPOINT')

def get_kafka_conn_object():
  for _ in range(3000):
    try:
      time.sleep(5)
      return KafkaConsumer(KAFKA_TOPIC,
                          boostrap_servers=KAFKA_CONN,
                          auto_offset_reset='earliest',
                          group_id='my_group',
                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    except:
      print('Trying to connect to kafka')

kafka_cons = get_kafka_conn_object()

for message in kafka_cons:
  r = requests.post(PRODUCER_ENDPOINT, json.dumps({'topic': message.topic, 'message': message.value}))
  print(r.status_code)
