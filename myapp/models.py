from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CAT=((1, 'Premium'),(2,'Analogue'),(3,'Digital'))
    name=models.CharField(max_length=50,verbose_name="Product Name")
    price=models.IntegerField()
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    pdetails=models.CharField(max_length=50,verbose_name="Product Details")
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="image")

class Cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amount=models.FloatField()