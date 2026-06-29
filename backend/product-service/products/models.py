from django.db import models
from abc import abstractmethod


# stores product categories — creates table: products_category
class Category(models.Model):
    # unique=True ensures no duplicate category names
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    # auto set when category is created, never changes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# abstract = True — no table created for this class, only a blueprint
# all child classes inherit these common fields
class BaseProduct(models.Model):
    name = models.CharField(max_length=200)
    # unique product identifier used in inventory tracking
    sku = models.CharField(max_length=200, unique=True)
    # max_digits=10, decimal_places=2 — supports prices like 99999999.99
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # links product to a category — SET_NULL keeps product if category is deleted
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # tells Django not to create a DB table for this class

    # child classes must implement this — Abstraction
    @abstractmethod
    def get_discount(self):
        pass

    # child classes must implement this — Abstraction
    @abstractmethod
    def get_product_type(self):
        pass

    # calls get_discount() internally — one function calling another — Polymorphism
    def get_discounted_price(self):
        discount = self.get_discount()
        return self.price - (self.price * discount/100)

    def __str__(self):
        return f"{self.name} - {self.sku}"


# creates table: products_electronicsproduct
# inherits all BaseProduct fields + adds brand, warranty_years
class ElectronicsProduct(BaseProduct):
    brand = models.CharField(max_length=100)
    warrenty_years = models.IntegerField(default=1)

    # Polymorphism — same method name, different discount than other product types
    def get_discount(self):
        return 10  # 10% discount for electronics

    def get_product_type(self):
        return "Electronics"


# creates table: products_foodproduct
# inherits all BaseProduct fields + adds expiry_date, is_organic
class FoodProduct(BaseProduct):
    expiry_date = models.DateField()
    is_organic = models.BooleanField(default=False)

    # Polymorphism — same method name, different discount than other product types
    def get_discount(self):
        return 5  # 5% discount for food

    def get_product_type(self):
        return "Food"


# creates table: products_clothingproduct
# inherits all BaseProduct fields + adds size, material
class ClothingProduct(BaseProduct):
    size = models.CharField(max_length=100)
    material = models.CharField(max_length=100)

    # Polymorphism — same method name, different discount than other product types
    def get_discount(self):
        return 20  # 20% discount for clothing

    def get_product_type(self):
        return "Clothing"
