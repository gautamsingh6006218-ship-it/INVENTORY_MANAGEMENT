from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from notifications.models import Notification


class NotificationListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/notifications/'

    def test_get_all_notifications(self):
        # create two notifications in test DB
        Notification.objects.create(user_id=1, message='Order shipped', notification_type='order', is_read=False)
        Notification.objects.create(user_id=2, message='Discount available', notification_type='discount', is_read=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both notifications
        self.assertEqual(len(response.data), 2)

    def test_create_notification(self):
        data = {
            'user_id': 1,
            'message': 'Your order has been delivered',
            'notification_type': 'order',
            'is_read': False
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Your order has been delivered')
        # is_read should be False by default
        self.assertEqual(response.data['is_read'], False)

    def test_create_notification_missing_fields(self):
        # user_id, message, notification_type are required — should return 400
        data = {'user_id': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NotificationDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a notification to use in all detail tests
        self.notification = Notification.objects.create(
            user_id=1, message='Stock low alert',
            notification_type='stock', is_read=False
        )
        self.url = f'/api/notifications/{self.notification.id}/'

    def test_get_single_notification(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Stock low alert')

    def test_get_notification_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/notifications/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_notification(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())


class MarkReadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.notification = Notification.objects.create(
            user_id=1, message='New discount available',
            notification_type='discount', is_read=False
        )
        self.url = f'/api/notifications/{self.notification.id}/mark-read/'

    def test_mark_notification_as_read(self):
        # notification starts as unread — mark it as read
        response = self.client.patch(self.url, {'is_read': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_read'], True)

    def test_mark_notification_as_unread(self):
        # set to read first, then mark as unread
        self.notification.is_read = True
        self.notification.save()
        response = self.client.patch(self.url, {'is_read': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_read'], False)

    def test_mark_read_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.patch('/api/notifications/9999/mark-read/', {'is_read': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
