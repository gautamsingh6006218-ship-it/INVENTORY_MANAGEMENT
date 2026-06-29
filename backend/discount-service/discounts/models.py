from django.db import models


class Discount(models.Model):
    code = models.CharField(max_length=100, unique=True)        # unique coupon code e.g. SAVE10
    discount_type = models.CharField(max_length=20)             # 'percentage' or 'fixed'
    value = models.DecimalField(max_digits=10, decimal_places=2)  # e.g. 10.00 means 10% or $10 off
    product_id = models.IntegerField()                          # IntegerField not ForeignKey — cross-service, no shared DB
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2)  # minimum order to apply discount
    is_active = models.BooleanField(default=True)               # False = discount deactivated
    valid_from = models.DateTimeField()                         # discount start date
    valid_until = models.DateTimeField()                        # discount expiry date
    created_at = models.DateTimeField(auto_now_add=True)        # set once on creation, never changes

    def __str__(self):
        return f"{self.code} - {self.discount_type}"
    
    
