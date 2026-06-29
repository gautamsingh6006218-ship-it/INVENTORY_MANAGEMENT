from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def supplier_list(request):
    if request.method == 'GET':
        # fetch all suppliers from DB
        suppliers = Supplier.objects.all()
        # many=True tells serializer multiple objects are being converted to JSON
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # saves new supplier to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def supplier_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/suppliers/1/ → pk=1
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        # return 404 if no supplier with that ID exists in DB
        return Response({'message': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    if request.method == 'PUT':
        # pass existing object + new data — serializer knows this is an UPDATE not a CREATE
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the existing DB row
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        supplier.delete()  # removes the row from DB
        return Response({'message': 'Supplier deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def toggle_active(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

    # get is_active from request body — default to True if not provided
    is_active_to_toggle = request.data.get('is_active', True)
    supplier.is_active = is_active_to_toggle
    supplier.save()  # last_updated auto updates on save    
    return Response({'message': 'Supplier updated', 'new_is_active': supplier.is_active})


