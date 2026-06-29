from rest_framework import serializers
from discounts.models import Discount

# converts Discount model to JSON and validates incoming discount data from frontend
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        # id and created_at are auto generated — returned in response but not required in request
        fields = ['id', 'code', 'discount_type', 'value', 'product_id', 'min_order_value', 'is_active', 'valid_from', 'valid_until', 'created_at']