import time
import json
from kafka import KafkaConsumer, KafkaProducer

TOPIC_NAME = 'users_info'

consumer = KafkaConsumer(
    TOPIC_NAME,
    auto_offset_reset='earliest', # where to start reading the messages at
    group_id='event-collector-group-1', # consumer group id
    bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
    security_protocol= 'PLAINTEXT'
)

producer = KafkaProducer(bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'], max_block_ms=5000)
for message in consumer:
    message.value['insert_into_database_timestamp']=time.time()
    print(message.value)
    producer.send('processed_once', json.dumps(message.value).encode('utf-8'))

