from django.db import models


class Report(models.Model):
    report_type = models.CharField(max_length=50)           # e.g. 'sales', 'inventory', 'orders'
    status = models.CharField(max_length=20, default='pending')  # 'pending', 'completed', 'failed'
    data = models.JSONField()                               # stores the report result as JSON
    created_by = models.IntegerField()                      # IntegerField not ForeignKey — user lives in user-service (separate DB)
    generated_at = models.DateTimeField(auto_now_add=True)  # set once when report is created, never changes

    def __str__(self):
        return f"{self.report_type} - {self.status}"
    