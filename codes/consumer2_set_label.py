from faker import Faker
import json
from kafka import KafkaConsumer, KafkaProducer

TOPIC_NAME = 'processed_once'

consumer = KafkaConsumer(
    TOPIC_NAME,
    auto_offset_reset='earliest', # where to start reading the messages at
    group_id='event-collector-group-2', # consumer group id
    bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
    security_protocol= 'PLAINTEXT'
)

producer = KafkaProducer(bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'], max_block_ms=5000)
fake = Faker()
for message in consumer:
    message.value['status']='looking for job' if fake.random_int(0, 1) == 1 else 'hired'
    print(message.value)
    producer.send('processed_twice', json.dumps(message.value).encode('utf-8'))