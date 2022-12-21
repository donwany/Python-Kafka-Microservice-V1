import json
import logging
from send.email import notification

from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)

ORDER_PROCESSED_KAFKA_TOPIC = "order-processed"

consumer = KafkaConsumer(
    ORDER_PROCESSED_KAFKA_TOPIC,
    bootstrap_servers="kafka-local.orders-microservice.svc.cluster.local:9092"
)

if __name__ == '__main__':
    emails_sent = set()
    logging.info("Started sending emails...")
    while True:
        for message in consumer:
            consumed_message = json.loads(message.value.decode('utf-8'))
            customer_email = consumed_message["email"]
            logging.info(f"Sending email to: {customer_email}")
            emails_sent.add(customer_email)
            logging.info(f"Number of Emails sent: {len(emails_sent)}")

            # send real email
            # notification(consumed_message)
