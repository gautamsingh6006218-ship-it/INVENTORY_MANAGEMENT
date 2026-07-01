from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer

CACHE_KEY = 'suppliers:list'


@api_view(['GET', 'POST'])
def supplier_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def supplier_detail(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return Response({'message': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        supplier.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Supplier deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def toggle_active(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

    supplier.is_active = request.data.get('is_active', True)
    supplier.save()
    cache.delete(CACHE_KEY)
    return Response({'message': 'Supplier updated', 'new_is_active': supplier.is_active})
