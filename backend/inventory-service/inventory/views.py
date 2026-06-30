from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from inventory.models import Stock
from inventory.serializers import StockSerializer
from kafka import KafkaProducer
from decouple import config
import json

# producer created at startup — try/except so Django can start even if Kafka isn't ready yet
try:
    producer = KafkaProducer(
        bootstrap_servers=config('KAFKA_BROKER', default='localhost:9092'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception:
    producer = None


# handles listing all stock entries and creating a new one
@api_view(['GET', 'POST'])
def inventory_list(request):
    if request.method == 'GET':
        # fetch all stock records from DB
        stocks = Stock.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new stock entry to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles GET, PUT, DELETE for a single stock entry by its ID
@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/inventory/1/ → pk=1
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        # return 404 if no stock entry with that ID exists in DB
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        stock.delete()  # removes the row from DB
        return Response({'message': 'Stock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# increases stock quantity — called when new stock arrives in warehouse
@api_view(['PUT'])
def add_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    # get quantity from request body — default to 0 if not provided
    quantity_to_add = request.data.get('quantity', 0)
    stock.quantity += int(quantity_to_add)  # add to existing quantity
    stock.save()  # last_updated auto updates on save

    if producer:
        try:
            # notify other services that stock was replenished
            producer.send('stock.added', {
                'product_id': stock.product_id,
                'quantity_added': int(quantity_to_add),
                'new_quantity': stock.quantity,
                'message': f"Stock added for product {stock.product_id}: +{quantity_to_add} units"
            })
        except Exception:
            # if Kafka is down, stock is still saved — event just won't be sent
            pass

    return Response({'message': 'Stock updated', 'new_quantity': stock.quantity})


# decreases stock quantity — called when an order is placed
@api_view(['PUT'])
def reduce_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity_to_reduce = request.data.get('quantity', 0)
    # prevent reducing more than what is available in stock
    if int(quantity_to_reduce) > stock.quantity:
        return Response({'error': 'Insufficient quantity'}, status=status.HTTP_400_BAD_REQUEST)

    stock.quantity -= int(quantity_to_reduce)  # subtract from existing quantity
    stock.save()  # last_updated auto updates on save

    # check if quantity has dropped to or below the reorder threshold
    if producer and stock.quantity <= stock.reorder_level:
        try:
            # alert other services that this product needs restocking
            producer.send('stock.low', {
                'product_id': stock.product_id,
                'current_quantity': stock.quantity,
                'reorder_level': stock.reorder_level,
                'message': f"Low stock alert for product {stock.product_id}: only {stock.quantity} units left"
            })
        except Exception:
            # if Kafka is down, stock is still reduced — alert just won't be sent
            pass

    return Response({'message': 'Stock reduced', 'new_quantity': stock.quantity})
