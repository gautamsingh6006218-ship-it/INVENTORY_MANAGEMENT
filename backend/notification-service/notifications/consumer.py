from kafka import KafkaConsumer
import json
import django
import os
import sys

# add project root to path so Django can find notification_service settings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# initialize Django so we can use models outside of the web server
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')
django.setup()

from notifications.models import Notification

# connect to Kafka and listen to order.created topic
consumer = KafkaConsumer(
    'order.created',                          # must match the topic producer publishes to
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print('Consumer started — listening for order events...')

# loop forever — processes each message as it arrives
for message in consumer:
    data = message.value
    print(f"Received event: {data}")
    # save notification to DB for the customer who placed the order
    Notification.objects.create(
        user_id=data['customer_id'],
        message=data['message'],
        notification_type='order',
        is_read=False
    )
    print(f"Notification saved for customer {data['customer_id']}")
    