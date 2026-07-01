from django.shortcuts import render
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.models import Category, ElectronicsProduct, FoodProduct, ClothingProduct
from products.serializers import CategorySerializer, ElectronicsSerializer, FoodSerializer, ClothingSerializer

# Create your views here.

# handles both listing and creating categories on same URL
@api_view(['GET', 'POST'])

def category_list(request):
    if request.method == 'GET':
        cached = cache.get('products:categories')
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        cache.set('products:categories', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products:categories')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles both listing and creating electronics products on same URL
@api_view(['GET', 'POST'])

def electronics_list(request):
    if request.method == 'GET':
        cached = cache.get('products:electronics')
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        products = ElectronicsProduct.objects.all()
        serializer = ElectronicsSerializer(products, many=True)
        cache.set('products:electronics', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ElectronicsSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            cache.delete('products:electronics')
            return Response({
                'message': 'Electronics Product created successfully',
                'product_type': product.get_product_type(),
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# handles both listing and creating food products on same URL
@api_view(['GET', 'POST'])

def food_list(request):
    if request.method == 'GET':
        cached = cache.get('products:food')
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        products = FoodProduct.objects.all()
        serializer = FoodSerializer(products, many=True)
        cache.set('products:food', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            cache.delete('products:food')
            return Response({
                'message': 'Food Product created successfully',
                'product_type': product.get_product_type(),
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles both listing and creating clothing products on same URL
@api_view(['GET', 'POST'])

def clothing_list(request):
    if request.method == 'GET':
        cached = cache.get('products:clothing')
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        products = ClothingProduct.objects.all()
        serializer = ClothingSerializer(products, many=True)
        cache.set('products:clothing', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ClothingSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            cache.delete('products:clothing')
            return Response({
                'message': 'Clothing Product created successfully',
                'product_type': product.get_product_type(),
                'discounted_price': str(product.get_discounted_price()),
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# handles GET, PUT, DELETE for a single category by its ID
@api_view(['GET', 'PUT', 'DELETE'])

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
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products:categories')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()
        cache.delete('products:categories')
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single electronics product by its ID
@api_view(['GET', 'PUT', 'DELETE'])

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
        serializer = ElectronicsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products:electronics')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        cache.delete('products:electronics')
        return Response({'message': 'Electronics Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single food product by its ID
@api_view(['GET', 'PUT', 'DELETE'])

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
        serializer = FoodSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products:food')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        cache.delete('products:food')
        return Response({'message': 'Food Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles GET, PUT, DELETE for a single clothing product by its ID
@api_view(['GET', 'PUT', 'DELETE'])

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
        serializer = ClothingSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('products:clothing')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        cache.delete('products:clothing')
        return Response({'message': 'Clothing Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
