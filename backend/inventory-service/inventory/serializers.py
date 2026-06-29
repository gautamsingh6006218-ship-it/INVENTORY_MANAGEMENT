from rest_framework import serializers
from inventory.models import Stock

# converts Stock model to JSON and validates incoming stock data from request
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        # id and last_updated are auto generated — returned in response but not required in request
        fields = ['id', 'product_id', 'quantity', 'warehouse_location', 'reorder_level', 'last_updated']
