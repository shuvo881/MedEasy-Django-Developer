# Generated by Django 5.0 on 2023-12-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_price_order_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSED', 'Processed'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered')], default='Pending', max_length=20),
        ),
    ]
