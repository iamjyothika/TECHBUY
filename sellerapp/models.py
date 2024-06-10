# Create your models here.
from django.db import models
from django.utils import timezone

from adminapp.models import *

from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class SellerDataModel(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_licence = models.CharField(max_length=255)
    seller_company_name = models.CharField(max_length=50)
    seller_phone = models.CharField(max_length=15)
    seller_address = models.TextField(max_length=255)
    seller_email = models.CharField(max_length=100)
    seller_pan = models.CharField(max_length=20)
    seller_gst = models.CharField(max_length=50)
    seller_bank_acc = models.CharField(max_length=50)
    seller_IFSC = models.CharField(max_length=50)
    seller_status = models.CharField(max_length=7, default='active')

    class Meta:
        db_table='seller_data_model'
    def __str__(self):
        return self.seller_company_name





class ProductModel(models.Model):
    product_id = models.IntegerField(primary_key=True)
    seller = models.ForeignKey(SellerDataModel, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_brand = models.CharField(max_length=25)
    product_description = models.TextField(max_length=600)
    product_price = models.IntegerField()
    seller_product_quantity = models.IntegerField()
    product_rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True)
    product_status = models.CharField(max_length=7, default='active')
    class Meta:
        db_table='product_model'
    def __str__(self):
        return self.product_name

    def has_discount(self):
        latest_discount = self.latest_discount()
        if latest_discount is not None and latest_discount.event.status == 'Active' and latest_discount.event.discount_end_date > timezone.now():
            return self.productdiscounts.exists()
        else:
            return False

    def latest_discount(self):
        latest_discount = self.productdiscounts.all().order_by('-created_at').first()
        return latest_discount

    def discount_price(self):
        latest_discount = self.latest_discount()

        if latest_discount is not None and latest_discount.event.status == 'Active' and latest_discount.event.discount_end_date > timezone.now():
            discounted_price = self.product_price - latest_discount.discount_amount
            return discounted_price
        else:
            return self.product_price


class ProductImageModel(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='images', on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='Images')
    class Meta:
        db_table='product_image_model'

    def __str__(self):
        return self.product.product_name


class PCSpecificationModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='pc', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    spec_ram = models.IntegerField()
    spec_processor = models.CharField(max_length=25)
    spec_storage = models.IntegerField()
    spec_gpu = models.CharField(max_length=20)
    spec_resolution = models.CharField(max_length=30)
    spec_display_size = models.IntegerField()
    spec_os = models.CharField(max_length=20)
    spec_refresh_rate = models.IntegerField()
    product_img = models.ForeignKey(ProductImageModel, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_status = models.CharField(max_length=7, default='active')
    class Meta:
        db_table='pc_specification_model'
    def __str__(self):
        return self.product.product_name


class SmartPhoneModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='phones', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    spec_ram = models.IntegerField()
    spec_processor = models.CharField(max_length=25)
    spec_storage = models.IntegerField()
    spec_resolution = models.CharField(max_length=30)
    spec_display_size = models.CharField(max_length=30)
    color = models.CharField(max_length=20)
    spec_battery = models.IntegerField()
    spec_camera = models.IntegerField()
    spec_os = models.CharField(max_length=10)
    product_img = models.ForeignKey(ProductImageModel,on_delete=models.CASCADE)
    warranty = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_status = models.CharField(max_length=7, default='active')

    class Meta:
        db_table = 'smartphone_specification_model'

    def __str__(self):
        return self.product.product_name

class TeleVisionModels(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='tv', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    spec_resolution = models.CharField(max_length=30)
    spec_display_size = models.IntegerField()
    spec_os = models.CharField(max_length=10)
    product_img = models.ForeignKey(ProductImageModel, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_status = models.CharField(max_length=7, default='active')
    class Meta:
        db_table = 'television_specification_model'

    def __str__(self):
        return self.product.product_name


class AudioModel(models.Model):
    specification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel,related_name='audio', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_type = models.TextField(max_length=50)
    spec_bluetooth = models.TextField(max_length=5)
    spec_playback = models.CharField(max_length=10)
    spec_mic = models.CharField(max_length=5)
    spec_latency = models.IntegerField()
    product_img = models.ForeignKey(ProductImageModel, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_status = models.CharField(max_length=7, default='active')
    class Meta:
        db_table = 'audio_specification_model'

    def __str__(self):
        return self.product.product_name



class ProductDiscount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    seller_id = models.ForeignKey(SellerDataModel, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,related_name='productdiscounts')
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    discount_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        db_table='product_discount_model'
    def __str__(self):
        return self.product.product_name
