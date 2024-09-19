"""
URL configuration for electronicsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from userapp import views
from adminapp import views as adminview
# from sellerapp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('category_name/<int:catg_id>',views.categories),
    path('about',views.aboutus,name="about"),
    path('contact',views.contact,name="contact"),
    path('product/<int:proid>',views.product,name="product"),
    path('search',views.search,name="search"),
    path('login',views.login,name="login"),
    path('dash',views.dash,name="dash"),
    path('account',views.myaccount,name="account"),
    path('cart',views.mycart,name="cart"),
    path('wish',views.wishlist,name="wishlist"),
    path('signup',views.register,name="signup"),
    path('logout',views.logout,name="logout"),
    path('address',views.myaddress,name="address"),
    path('showaddress',views.showaddress,name='showaddress'),
    path('update/<int:id>',views.updateaddress,name="editaddress"),
    path('cartremove/<int:id>',views.removecart),
    path('wishlistremove_/<int:id>', views.removewishlist),
    path('addressremove/<int:id>',views.removeaddress),
    path('addreview',views.addreview),
    path('userupdate',views.updateuser,name="updateuser"),
    path('buynow/<int:product_id>/', views.purchase_product, name='buynow'),




    path('adminhome',adminview.adminhome,name="adminhome"),
    path('adminshow',adminview.adminshow,name="showcategories"),
    path('productview',adminview.adminproduct,name="products"),
    path('productremove/<int:id>',adminview.productremove),
    path('userview',adminview.userview,name="userview")






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

