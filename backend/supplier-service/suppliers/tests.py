from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from suppliers.models import Supplier


class SupplierListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/suppliers/'

    def test_get_all_suppliers(self):
        # create two suppliers in test DB
        Supplier.objects.create(name='Supplier A', email='a@test.com', phone='1234567890', address='Addr A', product_id=1, supply_time_days=5, transport_mode='Air', rating=4.5, is_active=True)
        Supplier.objects.create(name='Supplier B', email='b@test.com', phone='0987654321', address='Addr B', product_id=2, supply_time_days=10, transport_mode='Sea', rating=3.8, is_active=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both suppliers
        self.assertEqual(len(response.data), 2)

    def test_create_supplier(self):
        data = {
            'name': 'Supplier C',
            'email': 'c@test.com',
            'phone': '1112223333',
            'address': 'Addr C',
            'product_id': 3,
            'supply_time_days': 7,
            'transport_mode': 'Road',
            'rating': '4.2',
            'is_active': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Supplier C')
        # is_active should default to True when not provided
        self.assertEqual(response.data['is_active'], True)

    def test_create_supplier_missing_fields(self):
        # name, email, product_id etc. are required — should return 400
        data = {'name': 'Incomplete Supplier'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SupplierDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a supplier to use in all detail tests
        self.supplier = Supplier.objects.create(
            name='Test Supplier', email='test@test.com', phone='9998887777',
            address='Test Address', product_id=1, supply_time_days=3,
            transport_mode='Air', rating=4.0, is_active=True
        )
        self.url = f'/api/suppliers/{self.supplier.id}/'

    def test_get_single_supplier(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Supplier')

    def test_get_supplier_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/suppliers/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_supplier(self):
        data = {
            'name': 'Updated Supplier',
            'email': 'updated@test.com',
            'phone': '1231231234',
            'address': 'Updated Address',
            'product_id': 2,
            'supply_time_days': 6,
            'transport_mode': 'Sea',
            'rating': '3.5',
            'is_active': True
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Supplier')
        self.assertEqual(response.data['transport_mode'], 'Sea')

    def test_delete_supplier(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())


class ToggleActiveTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.supplier = Supplier.objects.create(
            name='Toggle Supplier', email='toggle@test.com', phone='5556667777',
            address='Toggle Address', product_id=1, supply_time_days=4,
            transport_mode='Road', rating=4.8, is_active=True
        )
        self.url = f'/api/suppliers/{self.supplier.id}/toggle-active/'

    def test_toggle_active_to_false(self):
        # supplier starts as active — deactivate it
        response = self.client.patch(self.url, {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_active'], False)

    def test_toggle_active_to_true(self):
        # set to inactive first, then reactivate
        self.supplier.is_active = False
        self.supplier.save()
        response = self.client.patch(self.url, {'is_active': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_active'], True)

    def test_toggle_active_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.patch('/api/suppliers/9999/toggle-active/', {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
