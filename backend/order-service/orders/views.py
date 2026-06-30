from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from orders.serializers import OrderSerializer

# Create your views here.
@api_view(['GET', 'POST'])

def order_list(request):
    if request.method == 'GET':
        # fetch all orders from DB
        orders = Order.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new order to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])

def order_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/orders/1/ → pk=1
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        # return 404 if no order with that ID exists in DB
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        order.delete()  # removes the row from DB
        return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])

def update_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    # get status from request body — default to Pending if not provided
    status_to_update = request.data.get('status', 'Pending')
    order.status = status_to_update
    order.save()  # last_updated auto updates on save
    return Response({'message': 'Order updated', 'new_status': order.status})

