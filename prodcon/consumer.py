import json
from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer('order-details',
                         bootstrap_servers='kafka-local.orders-microservice.svc.cluster.local:9092')


if __name__ == '__main__':
    logging.info("Gonna start listening")
    while True:
        for message in consumer:
            logging.info("Here is a message..")
            logging.info(f"Received message: {json.loads(message.value.decode('utf-8'))}")
