from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)           # unique — no two suppliers share the same email
    phone = models.CharField(max_length=20)
    address = models.TextField()
    product_id = models.IntegerField()               # IntegerField not ForeignKey — supplier-service has its own DB
    supply_time_days = models.IntegerField()         # estimated days to deliver stock
    transport_mode = models.CharField(max_length=100)  # e.g. Air, Sea, Road
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g. 4.5 — max 3 digits, 1 decimal
    is_active = models.BooleanField(default=True)    # False = supplier deactivated, not deleted
    created_at = models.DateTimeField(auto_now_add=True)  # set once on creation, never changes

    def __str__(self):
        return f"{self.name} - {self.email}"