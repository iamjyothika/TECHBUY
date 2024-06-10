from django.db import models


# Create your models here.
class AdminRegistrationModel(models.Model):
    adm_ID = models.AutoField(primary_key=True)
    adm_username = models.CharField(max_length=20)
    adm_password = models.CharField(max_length=20)
    adm_email = models.CharField(max_length=50)
    adm_phone = models.CharField(max_length=15)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='admin_registration_model'
    def __str__(self):
        return self.adm_username


class ProductCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_img=models.ImageField(upload_to='categories',null=True)

    class Meta:
        db_table = 'product_category_model'

    def __str__(self):
        return self.category_name

class ProductBrandModel(models.Model):
    brand_id=models.AutoField(primary_key=True)
    category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    brand_name=models.CharField(max_length=255)
    brand_img=models.ImageField(upload_to='brandimgs')

    class Meta:
        db_table='product_brand_model'

    def __str__(self):
        return self.brand_name
class EventModel(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null=True)
    event_name = models.CharField(max_length=100)
    event_img = models.ImageField(upload_to='adbanners')
    discount_start_date = models.DateTimeField(auto_now_add=True)
    discount_end_date = models.DateTimeField()
    status = models.CharField(max_length=100,default='Active')
    class Meta:
        db_table='event_model'
    def __str__(self):
        return self.event_name

