from rest_framework import serializers
from suppliers.models import Supplier

# converts Supplier model to JSON and validates incoming supplier data from frontend
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        # id and created_at are auto generated — returned in response but not required in request
        fields = ['id', 'name', 'email', 'phone', 'address', 'product_id', 'supply_time_days', 'transport_mode', 'rating', 'is_active', 'created_at']