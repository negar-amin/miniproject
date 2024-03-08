import uuid
from datetime import datetime

def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    from kafka import KafkaProducer
    import time
    import logging
    import json

    producer = KafkaProducer(bootstrap_servers=['kafka1:9091','kafka2:9092','kafka3:9093'], max_block_ms=5000)

    try:
        res = get_data()
        res = format_data(res)
        res['id']=str(res['id'])
        print(res)
        producer.send('users_info', json.dumps(res).encode('utf-8'))
    except Exception as e:
        logging.error(f'An error occured: {e}')


stream_data()