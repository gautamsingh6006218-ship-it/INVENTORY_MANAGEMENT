from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from discounts.models import Discount


class DiscountListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/discounts/'

    def test_get_all_discounts(self):
        # create two discounts in test DB
        Discount.objects.create(code='SAVE10', discount_type='percentage', value=10.00, product_id=1, min_order_value=50.00, is_active=True, valid_from='2026-01-01T00:00:00Z', valid_until='2026-12-31T00:00:00Z')
        Discount.objects.create(code='FLAT20', discount_type='fixed', value=20.00, product_id=2, min_order_value=100.00, is_active=True, valid_from='2026-01-01T00:00:00Z', valid_until='2026-12-31T00:00:00Z')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both discounts
        self.assertEqual(len(response.data), 2)

    def test_create_discount(self):
        data = {
            'code': 'NEW15',
            'discount_type': 'percentage',
            'value': '15.00',
            'product_id': 1,
            'min_order_value': '75.00',
            'is_active': True,
            'valid_from': '2026-01-01T00:00:00Z',
            'valid_until': '2026-12-31T00:00:00Z'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 'NEW15')
        # is_active should default to True
        self.assertEqual(response.data['is_active'], True)

    def test_create_discount_missing_fields(self):
        # code, value, product_id etc. are required — should return 400
        data = {'code': 'INCOMPLETE'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DiscountDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a discount to use in all detail tests
        self.discount = Discount.objects.create(
            code='TEST10', discount_type='percentage', value=10.00,
            product_id=1, min_order_value=50.00, is_active=True,
            valid_from='2026-01-01T00:00:00Z', valid_until='2026-12-31T00:00:00Z'
        )
        self.url = f'/api/discounts/{self.discount.id}/'

    def test_get_single_discount(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'TEST10')

    def test_get_discount_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/discounts/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_discount(self):
        data = {
            'code': 'UPDATED20',
            'discount_type': 'fixed',
            'value': '20.00',
            'product_id': 2,
            'min_order_value': '100.00',
            'is_active': True,
            'valid_from': '2026-01-01T00:00:00Z',
            'valid_until': '2026-12-31T00:00:00Z'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'UPDATED20')
        self.assertEqual(response.data['discount_type'], 'fixed')

    def test_delete_discount(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Discount.objects.filter(id=self.discount.id).exists())


class ToggleActiveTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.discount = Discount.objects.create(
            code='TOGGLE10', discount_type='percentage', value=10.00,
            product_id=1, min_order_value=50.00, is_active=True,
            valid_from='2026-01-01T00:00:00Z', valid_until='2026-12-31T00:00:00Z'
        )
        self.url = f'/api/discounts/{self.discount.id}/toggle-active/'

    def test_toggle_active_to_false(self):
        # discount starts as active — deactivate it
        response = self.client.patch(self.url, {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_active'], False)

    def test_toggle_active_to_true(self):
        # set to inactive first, then reactivate
        self.discount.is_active = False
        self.discount.save()
        response = self.client.patch(self.url, {'is_active': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new_is_active'], True)

    def test_toggle_active_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.patch('/api/discounts/9999/toggle-active/', {'is_active': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
