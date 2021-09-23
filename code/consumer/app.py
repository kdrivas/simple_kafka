from kafka import KafkaConsumer
import requests
import os
import time
import json
import sys

KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PORT = os.getenv('KAFKA_PORT')
KAFKA_CONN = KAFKA_SERVER + ':' + KAFKA_PORT
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
PRODUCER_ENDPOINT = os.getenv('PRODUCER_ENDPOINT')

print('KAFKA_CONN', KAFKA_CONN)
print('KAFKA_TOPIC', KAFKA_TOPIC)

def wait_for_host(endpoint, timeout=100):
    i = 0
    while True:
        time.sleep(5)
        if (i > timeout):
            print("---> Timeout!")
            sys.exit()
        try:
            return requests.head(f"http://{endpoint}")
        except Exception:
            print("... Waiting for Producer ...")
            i += 1

def get_kafka_conn_object():
  for _ in range(20):
    try:
      time.sleep(5)
      return KafkaConsumer(KAFKA_TOPIC,
                          bootstrap_servers=KAFKA_CONN,
                          auto_offset_reset='earliest',
                          enable_auto_commit=False,
                          group_id='my_group',
                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    except:
      print('Trying to connect to kafka')

kafka_cons = get_kafka_conn_object()
wait_for_host(PRODUCER_ENDPOINT)

for message in kafka_cons:
  r = requests.post(f"http://{PRODUCER_ENDPOINT}/messages", data=json.dumps({'topic': message.topic, 'message': message.value}))
  print(r.status_code)
print('== Finish ==')