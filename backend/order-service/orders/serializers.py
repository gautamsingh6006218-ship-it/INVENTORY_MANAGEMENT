from rest_framework import serializers
from orders.models import Order


# converts between Order model and JSON — incoming: validates request data, outgoing: converts DB object to JSON
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # id and created_at are auto generated — returned in response but not required in request
        # status has default='Pending' in model — not required in request either
        fields = ['id', 'customer_id', 'product_id', 'quantity', 'total_price', 'status', 'created_at']
        