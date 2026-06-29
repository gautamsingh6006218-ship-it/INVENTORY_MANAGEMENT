from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from discounts.models import Discount
from discounts.serializers import DiscountSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def discount_list(request):
    if request.method == 'GET':
        # fetch all discounts from DB
        discounts = Discount.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new discount to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def discount_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/discounts/1/ → pk=1
        discount = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        # return 404 if no discount with that ID exists in DB
        return Response({'message': 'Discount not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        discount.delete()  # removes the row from DB
        return Response({'message': 'Discount deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def toggle_active(request, pk):
    try:
        discount = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        return Response({'error': 'Discount not found'}, status=status.HTTP_404_NOT_FOUND)

    # get is_active from request body — default to True if not provided
    is_active_to_toggle = request.data.get('is_active', True)
    discount.is_active = is_active_to_toggle
    discount.save()  # last_updated auto updates on save    
    return Response({'message': 'Discount updated', 'new_is_active': discount.is_active})
