from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product, Review, Order
from rest_framework import status

User = get_user_model()
 

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # user authentication ensure by jwt token
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.access_token}')


class ProductViewSetTestCase(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        self.image = SimpleUploadedFile("test_image.jpg", content=b"file_content", content_type="image/jpeg")
        
    
    def test_product_list(self):
        response = self.client.get('/products/api/products/')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': 15,
            'image': self.image,
            'is_sell': True,
        }
        #print(data['image'])
        response = self.client.post('/products/api/products/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReviewViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='Test Product', description='Test description', price=20, 
                                              image='product_images/test_image.jpg', is_sell=True)

    def test_review_list(self):
        response = self.client.get('/products/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        data = {
            'product': self.product.id,
            'comment': 'Great product!',
        }
        response = self.client.post('/products/api/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
    
    def test_update_review(self):
        updated_data = {'product': self.product.id, 'comment': 'Updated comment'}
        self.review = Review.objects.create(user=self.user, product=self.product, comment='Great product!')
        response = self.client.patch(f'/products/api/reviews/{self.review.id}/', data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the review from the database
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'Updated comment')
        
    def test_delete_review(self):
        self.review = Review.objects.create(user=self.user, product=self.product, comment='Great product!')
        response = self.client.delete(f'/products/api/reviews/{self.review.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the review was deleted from the database
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=self.review.id)

class OrderViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(name='Test Product', description='Test description', 
                                              image='product_images/test_image.jpg', price=30, is_sell=True)

    def test_order_list(self):
        response = self.client.get('/products/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {
            'product': self.product.id,
            'quantity': 2,
            'status': 'SHIPPED',
        }
        response = self.client.post('/products/api/orders/', data)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        
    def test_update_order(self):
        updated_data = {
                        "quantity": 200,
                        "status": "PENDING",
                        "product": self.product.id
                        }
        self.order = Order.objects.create(product= self.product, quantity=20, status=Order.status, user=self.user)
        response = self.client.patch(f'/products/api/orders/{self.order.id}/', data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the order from the database
        self.order.refresh_from_db()
        self.assertEqual(self.order.quantity, 200)
      