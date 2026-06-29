from rest_framework import serializers
from products.models import Category, ElectronicsProduct, FoodProduct, ClothingProduct

# converts Category model to JSON and validates incoming category data from frontend
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # id and created_at are auto generated — returned in response but not required in request
        fields = ["id", "name", "description", "created_at"]

# converts ElectronicsProduct to JSON — has electronics specific fields brand and warrenty_years
class ElectronicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicsProduct
        # category is a foreign key — sends category id in request, returns category id in response
        fields = ['id', 'name', 'sku', 'price', 'brand', 'warrenty_years', 'category', 'created_at']

# converts FoodProduct to JSON — has food specific fields expiry_date and is_organic
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ["id", "name", "sku", "price", "expiry_date", "is_organic", "category", "created_at"]

# converts ClothingProduct to JSON — has clothing specific fields size and material
class ClothingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothingProduct
        fields = ["id", "name", "sku", "price", "size", "material", "category", "created_at"]
