from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Category, ElectronicsProduct, FoodProduct, ClothingProduct


class CategoryListTests(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests without running a real server
        self.client = APIClient()
        self.url = '/api/products/categories/'

    def test_get_all_categories(self):
        # create two categories in test DB
        Category.objects.create(name='Electronics', description='Electronic items')
        Category.objects.create(name='Food', description='Food items')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # should return both categories
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        data = {'name': 'Clothing', 'description': 'Clothing items'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Clothing')

    def test_create_category_missing_name(self):
        # name is required — should return 400
        data = {'description': 'No name provided'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_category(self):
        # name has unique=True in model — duplicate should fail
        Category.objects.create(name='Electronics')
        data = {'name': 'Electronics'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CategoryDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create a category to use in all detail tests
        self.category = Category.objects.create(name='Electronics', description='Electronic items')
        self.url = f'/api/products/categories/{self.category.id}/'

    def test_get_single_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

    def test_get_category_not_found(self):
        # ID 9999 does not exist — should return 404
        response = self.client.get('/api/products/categories/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        data = {'name': 'Electronics Updated', 'description': 'Updated desc'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics Updated')

    def test_delete_category(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # confirm it no longer exists in DB
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class ElectronicsListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/products/electronics/'
        # electronics product requires a category foreign key
        self.category = Category.objects.create(name='Electronics')

    def test_get_all_electronics(self):
        ElectronicsProduct.objects.create(
            name='Laptop', sku='LAP001', price=999.99,
            brand='Dell', warrenty_years=2, category=self.category
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_electronics(self):
        data = {
            'name': 'Phone', 'sku': 'PHN001', 'price': '599.99',
            'brand': 'Apple', 'warrenty_years': 1, 'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # verify polymorphism methods work
        self.assertEqual(response.data['product_type'], 'Electronics')
        self.assertIn('discounted_price', response.data)

    def test_create_electronics_missing_fields(self):
        # sku and price are required — should return 400
        data = {'name': 'Phone', 'brand': 'Apple'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ElectronicsDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.product = ElectronicsProduct.objects.create(
            name='Laptop', sku='LAP001', price=999.99,
            brand='Dell', warrenty_years=2, category=self.category
        )
        self.url = f'/api/products/electronics/{self.product.id}/'

    def test_get_single_electronics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_get_electronics_not_found(self):
        response = self.client.get('/api/products/electronics/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_electronics(self):
        data = {
            'name': 'Laptop Pro', 'sku': 'LAP001', 'price': '1299.99',
            'brand': 'Dell', 'warrenty_years': 3, 'category': self.category.id
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop Pro')

    def test_delete_electronics(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ElectronicsProduct.objects.filter(id=self.product.id).exists())


class FoodListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/products/food/'
        self.category = Category.objects.create(name='Food')

    def test_get_all_food(self):
        FoodProduct.objects.create(
            name='Apple', sku='APL001', price=2.99,
            expiry_date='2026-12-31', is_organic=True, category=self.category
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_food(self):
        data = {
            'name': 'Banana', 'sku': 'BAN001', 'price': '1.99',
            'expiry_date': '2026-12-31', 'is_organic': False, 'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_type'], 'Food')
        self.assertIn('discounted_price', response.data)

    def test_create_food_missing_expiry(self):
        # expiry_date is required — should return 400
        data = {'name': 'Banana', 'sku': 'BAN001', 'price': '1.99'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FoodDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Food')
        self.product = FoodProduct.objects.create(
            name='Apple', sku='APL001', price=2.99,
            expiry_date='2026-12-31', is_organic=True, category=self.category
        )
        self.url = f'/api/products/food/{self.product.id}/'

    def test_get_single_food(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Apple')

    def test_get_food_not_found(self):
        response = self.client.get('/api/products/food/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_food(self):
        data = {
            'name': 'Green Apple', 'sku': 'APL001', 'price': '3.99',
            'expiry_date': '2026-12-31', 'is_organic': True, 'category': self.category.id
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Green Apple')

    def test_delete_food(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FoodProduct.objects.filter(id=self.product.id).exists())


class ClothingListTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/products/clothing/'
        self.category = Category.objects.create(name='Clothing')

    def test_get_all_clothing(self):
        ClothingProduct.objects.create(
            name='T-Shirt', sku='TSH001', price=19.99,
            size='M', material='Cotton', category=self.category
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_clothing(self):
        data = {
            'name': 'Jeans', 'sku': 'JNS001', 'price': '49.99',
            'size': 'L', 'material': 'Denim', 'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_type'], 'Clothing')
        self.assertIn('discounted_price', response.data)

    def test_create_clothing_missing_fields(self):
        # size and material are required — should return 400
        data = {'name': 'Jeans', 'sku': 'JNS001', 'price': '49.99'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ClothingDetailTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Clothing')
        self.product = ClothingProduct.objects.create(
            name='T-Shirt', sku='TSH001', price=19.99,
            size='M', material='Cotton', category=self.category
        )
        self.url = f'/api/products/clothing/{self.product.id}/'

    def test_get_single_clothing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'T-Shirt')

    def test_get_clothing_not_found(self):
        response = self.client.get('/api/products/clothing/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_clothing(self):
        data = {
            'name': 'T-Shirt V2', 'sku': 'TSH001', 'price': '24.99',
            'size': 'L', 'material': 'Cotton', 'category': self.category.id
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'T-Shirt V2')

    def test_delete_clothing(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ClothingProduct.objects.filter(id=self.product.id).exists())
