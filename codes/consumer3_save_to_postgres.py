import psycopg2
import json
from kafka import KafkaConsumer

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="dblab",
    user="postgres",
    password="postgres123",
    host="postgres",  # assuming PostgreSQL container is running on localhost
    port="5432"        # default PostgreSQL port
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create a table (if it doesn't exist)
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(30),
    gender VARCHAR(6),
    address VARCHAR(100),
    post_code VARCHAR(20),
    email VARCHAR(100),
    username VARCHAR(50),
    dob VARCHAR(50),
    registered_date VARCHAR(50),
    phone VARCHAR(20),
    picture VARCHAR(100),
    insert_into_database_timestamp VARCHAR(50),
    status VARCHAR(15)
)
'''
cursor.execute(create_table_query)
conn.commit()

TOPIC_NAME = 'processed_twice'

consumer = KafkaConsumer(
    TOPIC_NAME,
    auto_offset_reset='earliest', # where to start reading the messages at
    group_id='event-collector-group-3', # consumer group id
    bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) ,# we deserialize our data from json
    security_protocol= 'PLAINTEXT'
)
print("Consumer Started ...")
for message in consumer:
    print(f"Value:{message.value}")
    # Insert data into the table
    insert_query = "INSERT INTO users VALUES ( %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_to_insert = [
        (message.value['id'],
         message.value['first_name'],
         message.value['last_name'],
         message.value['gender'],
         message.value['address'],
         message.value['post_code'],
         message.value['email'],
         message.value['username'],
         message.value['dob'],
         message.value['registered_date'],
         message.value['phone'],
         message.value['picture'],
         message.value['insert_into_database_timestamp'],
         message.value['status']
        )
    ]
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
