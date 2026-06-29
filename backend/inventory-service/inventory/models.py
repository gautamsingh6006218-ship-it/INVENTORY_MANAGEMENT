from django.db import models


# stores stock levels for each product in the warehouse
class Stock(models.Model):
    # IntegerField not ForeignKey — product lives in a separate DB (product-service)
    # microservices cannot have FK relationships across different databases
    product_id = models.IntegerField()

    # current number of units available in warehouse
    quantity = models.IntegerField(default=0)

    # physical location in warehouse e.g. "Aisle 3, Shelf B"
    warehouse_location = models.CharField(max_length=200)

    # when quantity drops below this number, a restock alert should be triggered
    reorder_level = models.IntegerField(default=10)

    # auto updates every time the stock record is saved — tracks last stock change
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.product_id} - Qty: {self.quantity}"
    