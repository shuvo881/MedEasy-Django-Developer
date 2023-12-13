from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 150)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(limit_value=0)])
    image = models.ImageField(upload_to='product_images/')
    is_sell = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=0)])    
    
    def __str__(self):
        return f'{self.user} {self.product}'
    
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f'{self.user} {self.product}'
    

