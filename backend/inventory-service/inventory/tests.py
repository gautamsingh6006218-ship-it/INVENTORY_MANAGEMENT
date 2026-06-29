from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import Stock


class InventoryListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/inventory/'

    def test_get_all_stock(self):
        # create two stock entries in test DB
        Stock.objects.create(product_id=1, quantity=50, warehouse_location='Aisle 1', reorder_level=10)
        Stock.objects.create(product_id=2, quantity=30, warehouse_location='Aisle 2', reorder_level=5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both stock entries
        self.assertEqual(len(response.data), 2)

    def test_create_stock(self):
        data = {
            'product_id': 1,
            'quantity': 50,
            'warehouse_location': 'Aisle 3, Shelf B',
            'reorder_level': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_id'], 1)
        self.assertEqual(response.data['quantity'], 50)

    def test_create_stock_missing_fields(self):
        # product_id and warehouse_location are required — should return 400
        data = {'quantity': 50}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InventoryDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a stock entry to use in all detail tests
        self.stock = Stock.objects.create(
            product_id=1, quantity=50,
            warehouse_location='Aisle 3, Shelf B', reorder_level=10
        )
        self.url = f'/api/inventory/{self.stock.id}/'

    def test_get_single_stock(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], 1)

    def test_get_stock_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/inventory/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_stock(self):
        data = {
            'product_id': 1,
            'quantity': 100,
            'warehouse_location': 'Aisle 5, Shelf A',
            'reorder_level': 20
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 100)
        self.assertEqual(response.data['warehouse_location'], 'Aisle 5, Shelf A')

    def test_delete_stock(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Stock.objects.filter(id=self.stock.id).exists())


class AddStockTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.stock = Stock.objects.create(
            product_id=1, quantity=50,
            warehouse_location='Aisle 3, Shelf B', reorder_level=10
        )
        self.url = f'/api/inventory/{self.stock.id}/add-stock/'

    def test_add_stock(self):
        # quantity was 50, adding 20 should make it 70
        response = self.client.put(self.url, {'quantity': 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_quantity'], 70)

    def test_add_stock_not_found(self):
        response = self.client.put('/api/inventory/9999/add-stock/', {'quantity': 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_zero_stock(self):
        # adding 0 should keep quantity the same
        response = self.client.put(self.url, {'quantity': 0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_quantity'], 50)


class ReduceStockTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.stock = Stock.objects.create(
            product_id=1, quantity=50,
            warehouse_location='Aisle 3, Shelf B', reorder_level=10
        )
        self.url = f'/api/inventory/{self.stock.id}/reduce-stock/'

    def test_reduce_stock(self):
        # quantity was 50, reducing by 20 should make it 30
        response = self.client.put(self.url, {'quantity': 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_quantity'], 30)

    def test_reduce_stock_not_found(self):
        response = self.client.put('/api/inventory/9999/reduce-stock/', {'quantity': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reduce_stock_insufficient_quantity(self):
        # trying to reduce more than available — should return 400
        response = self.client.put(self.url, {'quantity': 100}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Insufficient quantity')
