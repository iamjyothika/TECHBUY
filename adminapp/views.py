from django.shortcuts import render,redirect
from sellerapp.models import *
from adminapp.models import *
from userapp.models import *

# Create your views here.
def adminhome(request):
    product=ProductModel.objects.all().count()
    return render(request,"adminhome.html",{"productcount":product})

def adminshow(request):
    show=ProductCategory.objects.all()
    product = ProductModel.objects.all().count()
    return render(request,"viewingcategories.html",{"category":show,"productcount":product})

def adminproduct(request):
    product = ProductModel.objects.all().count()
    viewproduct=ProductModel.objects.all()
    return render(request,"viewingproducts.html",{"items":viewproduct,"productcount":product})

def productremove(request,id):
    remove=ProductModel.objects.get(product_id=id)
    remove.delete()
    return redirect('productview')

def userview(request):
    product = ProductModel.objects.all().count()
    user=UserDataModel.objects.all()
    return render(request,"viewingusers.html",{"users":user,"productcount":product})
