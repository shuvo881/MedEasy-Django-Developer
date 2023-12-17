from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from products.models import Product, Order, Review

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=10,
            image= 'product_images/test_image.jpg',
            is_sell=True
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test description')
        self.assertEqual(product.price, 10)
        self.assertEqual(product.image, 'product_images/test_image.jpg')
        self.assertTrue(product.is_sell)

    def test_product_str_representation(self):
        product = Product.objects.create(name='Test Product', description='Test description', price=10, 
                                         image='product_images/test_image.jpg', is_sell=True)
        self.assertEqual(str(product), 'Test Product')

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', description='Test description', price=10, 
                                              image='product_images/test_image.jpg', is_sell=True)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            status=Order.STATUS_CHOICES['PENDING']
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.status, Order.STATUS_CHOICES['PENDING'])

    def test_order_str_representation(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=2, status=Order.STATUS_CHOICES['PENDING'])
        expected_str = f'{self.user} {self.product}'
        self.assertEqual(str(order), expected_str)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', description='Test description', price=10, 
                                              image='product_images/test_image.jpg', is_sell=True)

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            comment='Great product!'
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.comment, 'Great product!')

    def test_review_str_representation(self):
        review = Review.objects.create(user=self.user, product=self.product, comment='Great product!')
        expected_str = f'{self.user} {self.product}'
        self.assertEqual(str(review), expected_str)
