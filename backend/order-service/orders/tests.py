from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import Order


class OrderListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/orders/'

    def test_get_all_orders(self):
        # create two orders in test DB
        Order.objects.create(customer_id=1, product_id=1, quantity=2, total_price=199.99)
        Order.objects.create(customer_id=2, product_id=2, quantity=1, total_price=99.99)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both orders
        self.assertEqual(len(response.data), 2)

    def test_create_order(self):
        data = {
            'customer_id': 1,
            'product_id': 1,
            'quantity': 2,
            'total_price': '199.99'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_id'], 1)
        # status should default to Pending when not provided
        self.assertEqual(response.data['status'], 'Pending')

    def test_create_order_missing_fields(self):
        # customer_id, product_id, quantity, total_price are all required — should return 400
        data = {'customer_id': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create an order to use in all detail tests
        self.order = Order.objects.create(
            customer_id=1, product_id=1,
            quantity=2, total_price=199.99
        )
        self.url = f'/api/orders/{self.order.id}/'

    def test_get_single_order(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_id'], 1)

    def test_get_order_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/orders/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order(self):
        data = {
            'customer_id': 1,
            'product_id': 2,
            'quantity': 5,
            'total_price': '499.99'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 5)
        self.assertEqual(response.data['product_id'], 2)

    def test_delete_order(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())


class UpdateStatusTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(
            customer_id=1, product_id=1,
            quantity=2, total_price=199.99
        )
        self.url = f'/api/orders/{self.order.id}/status/'

    def test_update_status_to_shipped(self):
        # order starts as Pending — update to Shipped
        response = self.client.patch(self.url, {'status': 'Shipped'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_status'], 'Shipped')

    def test_update_status_to_delivered(self):
        response = self.client.patch(self.url, {'status': 'Delivered'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_status'], 'Delivered')

    def test_update_status_to_cancelled(self):
        response = self.client.patch(self.url, {'status': 'Cancelled'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_status'], 'Cancelled')

    def test_update_status_order_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.patch('/api/orders/9999/status/', {'status': 'Shipped'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
