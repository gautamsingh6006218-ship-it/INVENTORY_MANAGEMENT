from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from inventory.models import Stock
from inventory.serializers import StockSerializer
from kafka import KafkaProducer
from decouple import config
import json

try:
    producer = KafkaProducer(
        bootstrap_servers=config('KAFKA_BROKER', default='localhost:9092'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception:
    producer = None

CACHE_KEY = 'inventory:list'


@api_view(['GET', 'POST'])
def inventory_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        stock.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Stock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def add_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity_to_add = request.data.get('quantity', 0)
    stock.quantity += int(quantity_to_add)
    stock.save()
    cache.delete(CACHE_KEY)

    if producer:
        try:
            producer.send('stock.added', {
                'product_id': stock.product_id,
                'quantity_added': int(quantity_to_add),
                'new_quantity': stock.quantity,
                'message': f"Stock added for product {stock.product_id}: +{quantity_to_add} units"
            })
        except Exception:
            pass

    return Response({'message': 'Stock updated', 'new_quantity': stock.quantity})


@api_view(['PUT'])
def reduce_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity_to_reduce = request.data.get('quantity', 0)
    if int(quantity_to_reduce) > stock.quantity:
        return Response({'error': 'Insufficient quantity'}, status=status.HTTP_400_BAD_REQUEST)

    stock.quantity -= int(quantity_to_reduce)
    stock.save()
    cache.delete(CACHE_KEY)

    if producer and stock.quantity <= stock.reorder_level:
        try:
            producer.send('stock.low', {
                'product_id': stock.product_id,
                'current_quantity': stock.quantity,
                'reorder_level': stock.reorder_level,
                'message': f"Low stock alert for product {stock.product_id}: only {stock.quantity} units left"
            })
        except Exception:
            pass

    return Response({'message': 'Stock reduced', 'new_quantity': stock.quantity})
