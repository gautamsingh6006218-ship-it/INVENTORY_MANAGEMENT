from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from orders.serializers import OrderSerializer
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

CACHE_KEY = 'orders:list'


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            if producer:
                try:
                    producer.send('order.created', {
                        'order_id': serializer.data['id'],
                        'customer_id': serializer.data['customer_id'],
                        'message': f"Order {serializer.data['id']} has been placed"
                    })
                except Exception:
                    pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        order.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def update_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    order.status = request.data.get('status', 'Pending')
    order.save()
    cache.delete(CACHE_KEY)
    return Response({'message': 'Order updated', 'new_status': order.status})
