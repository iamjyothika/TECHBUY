from django.db import models
import sellerapp.models

# Create your models here.
from sellerapp.models import *
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class UserDataModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=15)
    user_email = models.CharField(max_length=100)
    user_profile=models.ImageField(upload_to='Images',null=True)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_status = models.CharField(max_length=7, default='active')

    class Meta:
        db_table='user_data_model'

    def __str__(self):
        return self.user_name


class UserAddressDataModel(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    house_address = models.CharField(max_length=100)
    city_address = models.TextField(max_length=50)
    state_address = models.TextField(max_length=50)
    pincode_address = models.IntegerField()
    phone_no=models.CharField(max_length=10,null=True)

    class Meta:
        db_table='user_address_model'
    def __str__(self):
        return self.user.user_name


class CartDataModel(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(default=1)

    class Meta:
        db_table='cart_model'
    def __str__(self):
        return self.user.user_name


class ReviewDataModel(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    user_review = models.TextField(max_length=255)
    user_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        db_table='review_model'
    def __str__(self):
        return self.product.product_name


class OrderDetailsModel(models.Model):
    user_order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddressDataModel, on_delete=models.CASCADE)
    user_order_quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    billing_ref_no = models.CharField(max_length=80)
    status = models.TextField(max_length=10)

    class Meta:
        db_table='order_model'

    def __str__(self):
        return self.user.user_name


class WishlistModel(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserDataModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    class Meta:
        db_table='wishlist_model'
    def __str__(self):
        return self.user.user_name

