# Code inspired from Confluent Cloud official examples library
# https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/producer.py

from confluent_kafka import Producer
import json
import ccloud_lib # Library not installed with pip but imported from ccloud_lib.py
import numpy as np
import time
import requests

url = "https://realstonks.p.rapidapi.com/TSLA"

headers = {
	"X-RapidAPI-Key": "a32c1cdcc0msha82c8aa1b82a46ap160546jsnf7179faee06d",
	"X-RapidAPI-Host": "realstonks.p.rapidapi.com"
}

# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "TESLA_price" 

# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer = Producer(producer_conf)

# Create topic if it doesn't already exist
ccloud_lib.create_topic(CONF, TOPIC)

try:
    # Starts an infinite while loop that produces random current temperatures
    while True:
        record_key = "TSLA"
        record_value = json.dumps(
                json.loads(requests.request("GET", url, headers=headers).text)['price']
        )
        print("Producing record: {}\t{}".format(record_key, record_value))

        # This will actually send data to your topic
        producer.produce(
            TOPIC,
            key=record_key,
            value=record_value,
        )
        time.sleep(1)

 # Interrupt infinite loop when hitting CTRL+C
except KeyboardInterrupt:
    pass
finally:
    producer.flush() # Finish producing the latest event before stopping the whole script
