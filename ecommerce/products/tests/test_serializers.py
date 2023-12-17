from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Product, Review, Order
from products.serializers import ProductSerializer, ReviewSerializer, OrderSerializer

User = get_user_model()

class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

class ProductSerializerTestCase(BaseAPITestCase):
    def test_product_serializer(self):
        product_data = {'name': 'Test Product', 'description': 'Test description', 'price': 15, 'is_sell': True}
        response = self.client.post('/api/products/', data=product_data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReviewSerializerTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='Test Product', description='Test description', price=20, is_sell=True)

    def test_review_serializer(self):
        review_data = {'product': self.product.id, 'comment': 'Great product!'}
        response = self.client.post('/api/reviews/', data=review_data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class OrderSerializerTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='Test Product', description='Test description', price=30, is_sell=True)

    def test_order_serializer(self):
        order_data = {'product': self.product.id, 'quantity': 2, 'status': 'Pending'}
        response = self.client.post('/api/orders/', data=order_data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)