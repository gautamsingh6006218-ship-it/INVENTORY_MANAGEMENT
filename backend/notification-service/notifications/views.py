from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

# handles GET all notifications and POST create new notification
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def notification_list(request):
    if request.method == 'GET':
        # fetch all notifications from DB
        notifications = Notification.objects.all()
        # many=True tells serializer to convert a list of objects, not just one
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # pass incoming JSON data to serializer for validation
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            # all fields valid — save new notification row to DB
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # validation failed — return errors so client knows what's wrong
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handles GET single notification and DELETE by ID
@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def notification_detail(request, pk):
    try:
        # pk comes from the URL — e.g. /api/notifications/1/ → pk=1
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        # no notification found with that ID — return 404
        return Response({'message': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # no data= argument — just reading, not updating
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    if request.method == 'DELETE':
        # remove the notification row from DB permanently
        notification.delete()
        return Response({'message': 'Notification deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# handles PATCH to mark a notification as read or unread
@api_view(['PATCH'])
@permission_classes([AllowAny])
def mark_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        # no notification found with that ID — return 404
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    # get is_read value from request body — default to False if not provided
    is_read_to_toggle = request.data.get('is_read', False)
    # update the is_read field and save to DB
    notification.is_read = is_read_to_toggle
    notification.save()
    return Response({'message': 'Notification updated', 'new_is_read': notification.is_read})

