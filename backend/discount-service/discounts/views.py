from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from discounts.models import Discount
from discounts.serializers import DiscountSerializer

CACHE_KEY = 'discounts:list'


@api_view(['GET', 'POST'])
def discount_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def discount_detail(request, pk):
    try:
        discount = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        return Response({'message': 'Discount not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        discount.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Discount deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def toggle_active(request, pk):
    try:
        discount = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        return Response({'error': 'Discount not found'}, status=status.HTTP_404_NOT_FOUND)

    discount.is_active = request.data.get('is_active', True)
    discount.save()
    cache.delete(CACHE_KEY)
    return Response({'message': 'Discount updated', 'new_is_active': discount.is_active})
