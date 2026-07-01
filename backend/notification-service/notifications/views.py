from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

CACHE_KEY = 'notifications:list'


@api_view(['GET', 'POST'])
def notification_list(request):
    if request.method == 'GET':
        cached = cache.get(CACHE_KEY)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        cache.set(CACHE_KEY, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def notification_detail(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'message': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    if request.method == 'DELETE':
        notification.delete()
        cache.delete(CACHE_KEY)
        return Response({'message': 'Notification deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def mark_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    notification.is_read = request.data.get('is_read', False)
    notification.save()
    cache.delete(CACHE_KEY)
    return Response({'message': 'Notification updated', 'new_is_read': notification.is_read})
