from django.db import models


class Notification(models.Model):
    # IntegerField not ForeignKey — user lives in user-service (separate DB)
    user_id = models.IntegerField()
    # the actual notification message shown to the user
    message = models.TextField()
    # category of notification e.g. 'order', 'discount', 'stock'
    notification_type = models.CharField(max_length=50)
    # False = unread, True = user has seen this notification
    is_read = models.BooleanField(default=False)
    # set once when notification is created, never changes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.notification_type}"
    