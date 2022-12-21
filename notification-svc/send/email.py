import json
import os
import smtplib
from email.message import EmailMessage
from .config import GMAIL_ADDRESS, GMAIL_PASSWORD


def notification(message):
    message = json.loads(message)

    sender_address = GMAIL_ADDRESS    # os.environ.get("GMAIL_ADDRESS")
    sender_password = GMAIL_PASSWORD  # os.environ.get("GMAIL_PASSWORD")

    receiver_address = message["email"]
    order_id = message['order_id']
    total_cost = message['total_cost']

    msg = EmailMessage()
    msg.set_content(f"order with id: {order_id} is now ready! with total cost of: ${total_cost}")
    msg["Subject"] = f"Your order {order_id} is ready to ship!"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent")
