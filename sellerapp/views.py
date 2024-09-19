from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.core.mail import send_mail

from .models import SellerDataModel, ProductModel
from .utils import send_otp
from django.contrib import messages
import pyotp
from datetime import datetime, timedelta
from django.db.models import Q
from sellerapp.models import *
from userapp.models import OrderDetailsModel
from adminapp.models import ProductCategoryModel

def home(request):
    if 'seller_id' in request.session:
        seller_id = request.session['seller_id']
        seller_obj = SellerDataModel.objects.get(seller_id=seller_id)
        product_data = ProductModel.objects.filter(seller=seller_obj)
        product_active = product_data.filter(product_status='active').count()
        product_inactive = product_data.filter(product_status='inactive').count()
        new_orders = OrderDetailsModel.objects.filter(product__seller__seller_id = seller_id ,status = 'dispatched').count()
        cancelled_orders = OrderDetailsModel.objects.filter(product__seller__seller_id = seller_id ,status = 'cancelled').count()
        low_stock=0
        no_stock=0
        for data in product_data:
            if data.seller_product_stock ==0:
                no_stock +=1
            elif data.seller_product_stock <=10:
                low_stock +=1
        return render (request,'Sellerdashboard.html',{'seller':seller_obj,'product_active':product_active,'product_inactive':product_inactive,'low_stock':low_stock,'no_stock':no_stock,'new_orders':new_orders,'cancelled_orders':cancelled_orders})
    else:
        return redirect('seller_login')


