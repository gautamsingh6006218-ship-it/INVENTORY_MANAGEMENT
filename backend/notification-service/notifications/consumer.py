from kafka import KafkaConsumer
from decouple import config
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

# listen to all three topics — order placed, stock added, stock low
# reads KAFKA_BROKER from .env — defaults to localhost:9092 for local dev, kafka:9092 in Docker
consumer = KafkaConsumer(
    'order.created',
    'stock.added',
    'stock.low',
    bootstrap_servers=config('KAFKA_BROKER', default='localhost:9092'),
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print('Consumer started — listening for order and stock events...')

# loop forever — processes each message as it arrives
for message in consumer:
    data = message.value
    # message.topic tells us which topic this message came from
    topic = message.topic
    print(f"Received [{topic}] event: {data}")

    if topic == 'order.created':
        # save notification for the customer who placed the order
        Notification.objects.create(
            user_id=data['customer_id'],
            message=data['message'],
            notification_type='order',
            is_read=False
        )
        print(f"Notification saved for customer {data['customer_id']}")

    elif topic == 'stock.added':
        # save notification for admin (user_id=1) when new stock arrives
        Notification.objects.create(
            user_id=1,
            message=data['message'],
            notification_type='stock',
            is_read=False
        )
        print(f"Stock added notification saved for product {data['product_id']}")

    elif topic == 'stock.low':
        # save urgent notification for admin when quantity drops below reorder_level
        Notification.objects.create(
            user_id=1,
            message=data['message'],
            notification_type='stock',
            is_read=False
        )
        print(f"Low stock notification saved for product {data['product_id']}")
