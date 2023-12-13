from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 150)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')
