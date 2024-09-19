import time

from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from sellerapp.models import *
from adminapp.models import *
from userapp.models import *
from sellerapp.models import *
from django.db.models import Q
import random


# Create your views here.
def home(request):
    def get_four_data(category):
        count = ProductModel.objects.filter(category_id__category_name=category).count()
        if count < 4:
            return ProductModel.objects.filter(category_id__category_name=category)
        random_index = random.randint(0, count - 4)
        return ProductModel.objects.filter(category_id__category_name=category)[random_index: random_index + 4]

    tv_data = get_four_data('Television')
    laptop_data = get_four_data('Laptops')
    phone_data = get_four_data('Mobiles')
    catg_data = ProductCategory.objects.all()
    event = EventModel.objects.all().order_by('-event_id')[:3]
    star_range = list(range(1, 6))
    return render(request, 'home.html',
                  {'mobile_data': phone_data, 'lap_data': laptop_data, 'tv_data': tv_data, 'categories': catg_data,
                   'event_data': event, 'star_range': star_range})


def categories(request, catg_id):
    brand = ProductBrandModel.objects.filter(category_id=catg_id)
    data = ProductCategory.objects.all()
    data1 = ProductModel.objects.filter(category_id=catg_id)
    ad = EventModel.objects.filter(event_category=catg_id)
    current_category_data = ProductCategory.objects.filter(category_id=catg_id)
    return render(request, 'categoriespage.html',
                  {'categories': data, 'brand_data': brand, 'product_data': data1, 'ad_data': ad,
                   'category_name': current_category_data})


def product(request, proid):
    data = ProductModel.objects.filter(product_id=proid)
    product_obj = get_object_or_404(ProductModel, product_id=proid)
    cat_id = ProductModel.objects.get(product_id=proid).category_id
    review = ReviewDataModel.objects.filter(product_id=proid)
    image = ProductImageModel.objects.filter(product_id=proid)
    current_product = ProductModel.objects.get(product_id=proid)
    similar_products = ProductModel.objects.filter(category=current_product.category).exclude(
        product_id=current_product.product_id)[:4]
    reviews = ReviewDataModel.objects.all()
    ratings = list(range(1, 6))

    user = None
    if "user" in request.session:
        user = UserDataModel.objects.get(user_id=request.session["user"])
    if request.method == "POST":
        if "user" in request.session:
            user1 = request.session["user"]
            if "addtocart" in request.POST:
                cart_obj = CartDataModel()
                cart_obj.user_id = user
                cart_obj.product = product_obj
                cart_obj.save()
            elif "wishlist" in request.POST:
                wish_obj = WishlistModel()
                wish_obj.user_id = user
                wish_obj.product = product_obj
                wish_obj.save()
        else:
            return redirect("/login")

    return render(request, "productdetails.html",
                  {'product_data': product_obj, 'cat_id': cat_id, 'review_data': review, 'image': image, "user": user,
                   "similar_products": similar_products, "ratings": ratings, "reviews": reviews})


def search(request):
    data = ProductModel.objects.all()
    if request.method == "POST":
        search_data = request.POST.get("search")
        detail = ProductModel.objects.filter(
            Q(product_name__icontains=search_data) | Q(category__category_name__icontains=search_data))
        return render(request, "searchdetails.html", {"item": detail})
    return render(request, "searchdetails.html", {"item": data})


def aboutus(request):
    return render(request, "aboutus.html")

def contact(request):
    user = None
    cart_no = None
    if 'user_id' in request.session:
        user = UserDataModel.objects.get(user_id=request.session['user_id'])
        cart_no = CartDataModel.objects.filter(user__user_id=request.session['user_id']).count()
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            send_mail(
                "Regarding your recent inquiry",
                f"Hi {name},"
                f"We have received your message ({message[:10]}...). Our representative will be contacting you soon.",
                "techbuy97@gmail.com",
                [email],
                fail_silently=False

            )
            return redirect('contact')

    return render(request, 'contactus.html', {'user': user, 'cart_no': cart_no})





def register(request):
    print("jj")
    if request.method == "POST":
        print("hello")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phonenumber")
        password = request.POST.get("password")
        password1 = request.POST.get("confirmpassword")
        if password != password1:
            print("hi")
            error = 'Passwords do not match'
            return render(request, 'signup.html', {'error': error})
        register_obj = UserDataModel()
        register_obj.user_name = username
        register_obj.user_email = email
        register_obj.user_password = password
        register_obj.user_phone = phone
        register_obj.save()
        return redirect('/login')
    return render(request, "signup.html")

def login(request):
    error = ''
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        user = UserDataModel.objects.filter(user_name=user_name, user_password=user_password).first()
        if user is not None:
            request.session['user'] = user.user_id
            return redirect('/')
        else:
            error = "invalid username and password"
    return render(request, 'login.html', {"error": error})


def dash(request):
    if "user" in request.session:
        userdata = request.session.get('user')
        data = UserDataModel.objects.filter(user_id=userdata)
        return render(request, "dashboard.html", {"user_data": data})
    else:
        return redirect("/login")





def mycart(request, product=None):
    if 'user' in request.session:
        userdata = request.session.get('user')
        user_instance = UserDataModel.objects.get(user_id=userdata)
        details = CartDataModel.objects.filter(user_id=userdata)
        cart_count = details.count()
        total_price = 0
        total_discount = 0
        for item in details:
            total_price += item.cart_quantity * item.product.product_price
        for i in details:
            if i.product.has_discount:
                discount_amount_per_product = i.product.product_price - i.product.discount_price()
                total_discount += i.cart_quantity * discount_amount_per_product
                print(total_discount)
        net_amount = total_price - total_discount
        if request.method == "POST":
            cart_id = request.POST.get('cart_id')
            product_data = request.POST.get('product_data')
            product = ProductModel.objects.get(product_id=product_data)
            cart_obj = CartDataModel.objects.get(cart_id=cart_id)

            if 'cart_add' in request.POST:
                cart_obj.cart_quantity += 1
            elif 'cart_min' in request.POST and cart_obj.cart_quantity > 0:
                cart_obj.cart_quantity -= 1

            cart_obj.user = user_instance
            cart_obj.product = product
            cart_obj.save()
            return redirect('cart')
        return render(request, "cart.html", {'cart_details': details,"cart_count":cart_count,'total_price':total_price,'total_discount':total_discount,'net_amount':net_amount,'product_obj':product})
    else:
        return redirect('/login')


def removecart(request, id):
    data = CartDataModel.objects.get(cart_id=id)
    data.delete()
    return redirect('/')


def wishlist(request):
    if 'user' in request.session:
        userdata = request.session.get('user')
        wishdata = WishlistModel.objects.filter(user_id=userdata)
        return render(request, "wishlist.html", {'wish_details': wishdata})
    else:
        return redirect('/login')


def removewishlist(request, id):
    data = WishlistModel.objects.get(wishlist_id=id)
    data.delete()
    return redirect('/')


def logout(request):
    print("logout fn called")
    try:
        del request.session['user']
        return redirect('/')
    except:
        return redirect('/')


def myaddress(request):
    if 'user' in request.session:
        print("jjj")
        user = UserDataModel.objects.get(user_id=request.session["user"])
        if request.method == "POST":
            house = request.POST.get("user-address")
            phone=request.POST.get("user-phone")
            pin = request.POST.get("user-pin")
            district = request.POST.get("user-district")
            state = request.POST.get("user-state")
            details = UserAddressDataModel()
            details.house_address = house
            details.phone_no=phone
            details.pincode_address = pin
            details.city_address = district
            details.state_address = state
            details.user = user
            details.save()
            return redirect('/showaddress')
        return render(request, 'myaddress.html')

    return redirect('/login')


def showaddress(request):
    print("show fn called")
    if 'user' in request.session:

        userdata = request.session.get('user')
        print(userdata)
        addressdata = UserAddressDataModel.objects.filter(user=UserDataModel.objects.get(user_id=userdata))
        return render(request, "myaddress.html", {'address': addressdata})
    else:
        return redirect('/login')


def updateaddress(request, id):
    if 'user' in request.session:
        user = UserDataModel.objects.get(user_id=request.session["user"])
        address = UserAddressDataModel.objects.filter(address_id=id)
        if request.method == "POST":
            house = request.POST.get("user-address")
            phone = request.POST.get("user-phone")
            pin = request.POST.get("user-pin")
            district = request.POST.get("user-district")
            state = request.POST.get("user-state")
            details = UserAddressDataModel.objects.get(address_id=id)
            details.house_address = house
            details.phone_no = phone
            details.pincode_address = pin
            details.city_address = district
            details.state_address = state
            details.user = user
            details.save()
            return redirect('/showaddress')
        return render(request, 'Edituseraddress.html', {'newaddress': address})
    return redirect('/login')


def removeaddress(request, id):
    remove = UserAddressDataModel.objects.get(address_id=id)
    remove.delete()
    return redirect('/showaddress')


def addreview(request):
    if 'user' in request.session:
        user = UserDataModel.objects.get(user_id=request.session["user"])
        if request.method == "POST":
            review = request.POST.get("review")
            rating = request.POST.get("rating")
            productid = request.POST.get("productid")
            reviews = ReviewDataModel()
            reviews.user_review = review
            reviews.user_rating = rating
            reviews.user = user
            reviews.product = ProductModel.objects.get(product_id=int(productid))
            reviews.save()
            return redirect(f'product/{productid}')
    else:
        return redirect('/login')

def myaccount(request):
    if "user" in request.session:
        userdata = request.session.get('user')
        data = UserDataModel.objects.filter(user_id=userdata)
        return render(request, "myaccount.html", {"userdata": data})
    else:
        return redirect("/login")



def updateuser(request):
    if 'user' in request.session:
        print("KKK")
        user = UserDataModel.objects.get(user_id=request.session["user"])
        userdata = request.session.get('user')
        data = UserDataModel.objects.filter(user_id=userdata)
        if request.method == "POST":
            print("hello")
            name = request.POST.get("username")
            email = request.POST.get("email")
            phone = request.POST.get("phno")
            data = UserDataModel.objects.get(user_id=request.session["user"])
            data.user_name = name
            data.user_email = email
            data.user_phone = phone
            data.user = user
            data.save()
            return redirect('/account')
        return render(request,"myaccount.html",{"userdata":data})

    return redirect('/login')
def purchase_product(request,product_id):
    request.session['product_session']=product_id
    if 'user' not in request.session:
        return redirect('/login')
    else:
        user_id=request.session['user']
        user=UserDataModel.objects.get(user_id=user_id)
        product_obj=ProductModel.objects.get(product_id=product_id)
        address_data=UserAddressDataModel.objects.filter(user=user)
        address_data_check=UserAddressDataModel.objects.filter(user=user)
        address_data_check = address_data.exists()
        current_address=None
        if address_data_check:
            first_address=address_data.first()
            request.session['address_id']=first_address.address_id
            address_id=int(request.session['address_id'])
            current_address=UserAddressDataModel.objects.get(address_id=address_id)
        if request.method=="POST":
            if 'del_add_change' in request.POST:
                selected_address_id=request.POST.get('address_input')
                request.session['address_id']=selected_address_id
                address_id=int(request.session['address_id'])
                current_address=UserAddressDataModel.objects.get(address_id=address_id)
            if 'quantity' in request.POST:
                quantity=int(request.POST.get('quantity'))
                request.session['quantity']=quantity

            total_price = product_obj.product_price * quantity
            total_discount_price = product_obj.discount_price() * quantity
            total_discount = total_price - total_discount_price

            last_order_data = OrderDetailsModel.objects.all().order_by('-user_order_id').first()
            if last_order_data is not None:
                last_ref_no = int(last_order_data.billing_ref_no) + 1
            else:
                last_ref_no = 100000





    return render(request,"buynow.html",{'user': user, 'product_obj': product_obj, 'discounted_price': total_discount_price,'quantity': quantity, 'total_price': total_price, 'total_discount': total_discount,'address_data':address_data, 'address_data_check':address_data_check , 'current_address': current_address})


