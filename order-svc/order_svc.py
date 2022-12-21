import json
import time
import uuid
import logging
import faker
import random
from datetime import datetime
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)

ORDER_KAFKA_TOPIC = "order-details"
ORDER_LIMIT = 15


def create_orders():
    f = faker.Faker()
    orders = dict(
        order_id=str(uuid.uuid4()),
        username=f.user_name(),
        first_name=f.first_name(),
        last_name=f.last_name(),
        email=f.email(),
        quantity=int(random.randint(1, 999)),
        price=round(float(random.uniform(10.5, 100.99)),2),
        date_created=str(datetime.utcnow())
    )
    return orders


producer = KafkaProducer(bootstrap_servers="kafka-local.orders-microservice.svc.cluster.local:9092")


if __name__ == '__main__':
    logging.info("Generating orders...")
    for i in range(ORDER_LIMIT):
        data = create_orders()
        producer.send(ORDER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
        logging.info(f"Done Sending..{i} - {data}")
        time.sleep(1)
