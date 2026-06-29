from django.db import models


# stores all customer orders — creates table: orders_order
class Order(models.Model):

    # IntegerField not ForeignKey — customer lives in user-service (separate DB)
    customer_id = models.IntegerField()

    # IntegerField not ForeignKey — product lives in product-service (separate DB)
    product_id = models.IntegerField()

    # number of units ordered
    quantity = models.IntegerField()

    # total cost of the order — max_digits=10, decimal_places=2 supports prices like 99999999.99
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # tracks where the order is in its lifecycle — starts as Pending by default
    status = models.CharField(max_length=200, default='Pending')

    # auto set when order is created, never changes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
    
