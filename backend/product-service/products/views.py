from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from products.models import Category, ElectronicsProduct, FoodProduct, ClothingProduct
from products.serializers import CategorySerializer, ElectronicsSerializer, FoodSerializer, ClothingSerializer

# Create your views here.

# handles both listing and creating categories on same URL
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def category_list(request):
    if request.method == 'GET':
        # fetch all categories from DB
        categories = Category.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new category to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles both listing and creating electronics products on same URL
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def electronics_list(request):
    if request.method == 'GET':
        # fetch all electronics products from DB
        products = ElectronicsProduct.objects.all()
        serializer = ElectronicsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ElectronicsSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # returns ElectronicsProduct Python object
            return Response({
                'message': 'Electronics Product created successfully',
                # get_product_type() — Polymorphism, returns "Electronics" from ElectronicsProduct class 
                'product_type': product.get_product_type(),
                # get_discounted_price() calls get_discount() internally — function calling function
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# handles both listing and creating food products on same URL
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def food_list(request):
    if request.method == 'GET':
        # fetch all food products from DB
        products = FoodProduct.objects.all()
        serializer = FoodSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # returns FoodProduct Python object
            return Response({
                'message': 'Food Product created successfully',
                # get_product_type() — Polymorphism, returns "Food" from FoodProduct class
                'product_type': product.get_product_type(),
                # get_discounted_price() calls get_discount() internally — function calling function
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles both listing and creating clothing products on same URL
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def clothing_list(request):
    if request.method == 'GET':
        # fetch all clothing products from DB
        products = ClothingProduct.objects.all()
        serializer = ClothingSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ClothingSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # returns ClothingProduct Python object
            return Response({
                'message': 'Clothing Product created successfully',
                # get_product_type() — Polymorphism, returns "Clothing" from ClothingProduct class
                'product_type': product.get_product_type(),
                # get_discounted_price() calls get_discount() internally — function calling function
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# handles GET, PUT, DELETE for a single category by its ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def category_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/products/categories/1/ → pk=1
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        # return 404 if no category with that ID exists in DB
        return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # serialize the single category object to JSON and return it
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()  # removes the row from DB
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single electronics product by its ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def electronics_detail(request, pk):
    try:
        # fetch the specific electronics product by primary key
        product = ElectronicsProduct.objects.get(pk=pk)
    except ElectronicsProduct.DoesNotExist:
        return Response({'message': 'Electronics Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument here — just reading, not updating
        serializer = ElectronicsSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        # passing both the existing product object and new request data triggers an update
        serializer = ElectronicsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Electronics Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single food product by its ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def food_detail(request, pk):
    try:
        # fetch the specific food product by primary key
        product = FoodProduct.objects.get(pk=pk)
    except FoodProduct.DoesNotExist:
        # return 404 if no food product with that ID exists in DB
        return Response({'message': 'Food Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument here — just reading, not updating
        serializer = FoodSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = FoodSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()  # removes the row from DB
        return Response({'message': 'Food Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single clothing product by its ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def clothing_detail(request, pk):
    try:
        # fetch the specific clothing product by primary key
        product = ClothingProduct.objects.get(pk=pk)
    except ClothingProduct.DoesNotExist:
        # return 404 if no clothing product with that ID exists in DB
        return Response({'message': 'Clothing Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument here — just reading, not updating
        serializer = ClothingSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = ClothingSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()  # removes the row from DB
        return Response({'message': 'Clothing Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
