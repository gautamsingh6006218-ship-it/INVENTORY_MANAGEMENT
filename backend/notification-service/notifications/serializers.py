from rest_framework import serializers
from notifications.models import Notification

# converts Notification model to JSON and validates incoming notification data from request
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        # tells serializer which model to work with
        model = Notification
        # id and created_at are auto generated — returned in response but not required in request
        fields = ['id', 'user_id', 'message', 'notification_type', 'is_read', 'created_at']
        