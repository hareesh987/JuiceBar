from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
import random
from .forms import *
from .models import *
from myapp.models import CustomUser
from django.http import JsonResponse
from .models import ImageUpload
from .forms import ImageUploadForm
from django.views.decorators.cache import never_cache


def homepage(request):
    data = Categories.objects.all()
    return render(request, 'homepage.html', {'data': data})

# def signup(request):
#     data=" "
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password')

#         if CustomUser.objects.filter(username=username).exists():
#             data="Username already taken. Choose a different one."
#             return render(request,'signup.html',{'data':data})
        
#         if CustomUser.objects.filter(email=email).exists():
#             data="Username already exists. Choose a different one."
#             return render(request,'signup.html',{'data':data})
        
#         user = CustomUser.objects.create_user(username=username, email=email, password=password1)
#         user.save()
#         return redirect('login')  
    
#     return render(request, 'signup.html',{'data':data})

def login_user(request):
    data=""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'myapp:homepage'))
        else:
            data="Invalid username or password"
            return render(request, 'login.html', {'data': data})
    
    return render(request, 'login.html',{'data':data})

def logout_user(request):
    logout(request)
    return redirect('myapp:homepage')

@never_cache    
def cartPage(request):
    if request.user.is_authenticated:
        data = cart.objects.filter(user=request.user)  
        total_items = sum(item.number for item in data)

        if not data:
            return render(request, 'cart.html', {'data': data, 'subtotal': 0, 'discount': 0, 'shipping': 0, 'totalprice': 0})

   
        subtotal = sum(item.price * item.number for item in data)

    
        total_discount = sum((item.price * item.number * item.product.Discount / 100) for item in data)

    
        discounted_price = subtotal - total_discount

        shipping = 50  
        totalprice = discounted_price + shipping  

        return render(request, 'cart.html', {
            'data': data,
            'total_items': total_items,
            'subtotal': subtotal,
            'discount': total_discount,
            'shipping': shipping,
            'totalprice': totalprice
        })
    else:
        return redirect('login')


@login_required(login_url='signup')
def orders(request):
    user_orders = Orders.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': user_orders})

# def milkshakes(request):

#     data = products.objects.filter(Category='milkshakes')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'milkshakes.html', {'data': data, 'cart_items': cart_items})

# def fruitjuices(request):
#     data = products.objects.filter(Category='fruitjuices')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'fruitjuices.html', {'data': data, 'cart_items': cart_items})

# def hotbeverages(request):
#     data = products.objects.filter(Category='hotbeverages')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'hotbeverages.html', {'data': data, 'cart_items': cart_items})

# def softdrinks(request):
#     data = products.objects.filter(Category='softdrinks')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'softdrinks.html', {'data': data, 'cart_items': cart_items})


# def energydrinks(request):
#     data = products.objects.filter(Category='energydrinks')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'energydrinks.html', {'data': data, 'cart_items': cart_items})

# def mocktails(request):
#     data = products.objects.filter(Category='mocktails')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'mocktails.html', {'data': data, 'cart_items': cart_items})

# def beers(request):
#     data = products.objects.filter(Category='beers')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'beers.html', {'data': data, 'cart_items': cart_items})

# def wines(request):
#     data = products.objects.filter(Category='wines')
#     cart_items = cart.objects.values_list('product_id', flat=True)
#     return render(request, 'wines.html', {'data': data, 'cart_items': cart_items})


def category_view(request, category_id):
    category_obj = get_object_or_404(Categories, id=category_id)

    data = products.objects.filter(Category=category_obj)

    cart_items = cart.objects.values_list('product_id', flat=True)

    return render(request, 'category.html', {'data': data, 'cart_items': cart_items, 'category': category_obj})

def addToCart(request, id):
    if request.user.is_authenticated:
        product = products.objects.get(id=id)
        cart.objects.create(
            user=request.user,  
            product=product, 
            image=product.image.url,  
            price=product.productPrice
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('login')  

def update_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id') 
        action = request.POST.get('action')
        cart_item = cart.objects.get(id=prod_id)  
        if action == "+":
            cart_item.number += 1
        elif action == "-" and cart_item.number > 1:
            cart_item.number -= 1
        cart_item.save() 
        return redirect('myapp:cartpage') 

def delete_item(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        cart_item = cart.objects.get(id=prod_id)
        cart_item.delete() 
        return redirect('myapp:cartpage')

def place_order(request):
    if request.user.is_authenticated:
        user_cart = cart.objects.filter(user=request.user)  

        if not user_cart:
            return redirect('myapp:cartpage')  
        
        for item in user_cart:
            Orders.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.number,
                price=item.price * item.number,
            )
        user_cart.delete()
        
        return redirect('myapp:orders')  
    else:
        return redirect('login')  

def offer_milk(request,d):
    data = products.objects.filter(Discount=d)
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request,'offer_milk.html',{"data":data, 'cart_items': cart_items})

otp_storage={}
def forgot_password(request):
    data=""
    if request.method == "POST":
        email = request.POST.get("email")
        User = get_user_model()  

        try:
            User.objects.get(email=email)  
            otp = random.randint(100000, 999999)  
            otp_storage[email] = otp

            send_mail(
                "Your OTP for Password Reset",
                f"Your OTP is: {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            request.session["reset_email"] = email 
            return redirect("verify_otp")

        except User.DoesNotExist:
            data="user Not exists"
            return render(request,"forgot.html",{'data':data})

    return render(request, "forgot.html")

def verify_otp(request):
    data = ""  
    email = request.session.get("reset_email")

    if not email:
        return redirect("forgot_password")  

    if request.method == "POST":
        user_otp = request.POST.get("otp")

        try:
            if otp_storage.get(email) == int(user_otp): 
                request.session["otp_verified"] = True
                otp_storage.pop(email, None)  
                return redirect("reset")
            else:
                data = "Invalid OTP"
        except ValueError:
            data = "OTP must be a number"

    return render(request, "verify_otp.html",{"data":data})

def reset_password(request):
    email = request.session.get("reset_email")
    User = get_user_model() 
    if not email or not request.session.get("otp_verified"):
        return redirect("forgot")

    if request.method == "POST":
        new_password = request.POST.get("password")
        user = User.objects.get(email=email)
        user.password = make_password(new_password)  
        user.save()

        del request.session["reset_email"]
        del request.session["otp_verified"]
        otp_storage.pop(email, None)  

        messages.success(request, "Password reset successful! Please log in.")
        return redirect("login")

    return render(request, "reset.html")


def owner_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Static username and password
        if username == "Owner@juicebar" and password == "Juicebar@123":
            print("valid")
            request.session["owner_logged_in"] = True  # Store login status in session
            return redirect('myapp:owner_home')
        else:
            print("invalid")
            return render(request, "login.html", {"error": "Invalid credentials!"})

    return render(request, "login.html")

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("owner_logged_in"):
            return redirect("myapp:owner_login")  # Redirect if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper

def logout_owner(request):
    request.session.flush()
    return redirect("myapp:owner_login")

@owner_required
def owner_home(request):
    categories = Categories.objects.all()
    data = products.objects.all()
    return render(request, "owner.html", {"categories": categories, "data": data})

@owner_required
def show_categories(request):
    data = Categories.objects.all()
    return render(request, "show_categories.html", {"data": data})

@owner_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            print("hello")
            form.save()
            return redirect("myapp:show_categories")
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

@owner_required
def edit_category(request, id):
    category = get_object_or_404(Categories, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            print("hello")
            form.save()
            return redirect("myapp:show_categories")
    else:
        print("rt")
        form = CategoryForm(instance=category)
    return render(request, "edit_category.html", {"form": form})

@owner_required
def delete_category(request, id):
    category = get_object_or_404(Categories, id=id)
    category.delete()
    return redirect("myapp:show_categories")


@owner_required
def show_products(request):
    data = products.objects.all()
    return render(request, "show_products.html", {"data": data})

@owner_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myapp:show_products")
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

@owner_required
def edit_product(request, id):
    product = get_object_or_404(products, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("myapp:show_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "edit_product.html", {"form": form})

@owner_required
def delete_product(request, id):
    product = get_object_or_404(products, id=id)
    product.delete()
    return redirect("myapp:show_products")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')

        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'data': "Username already taken. Choose a different one."})
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'data': "Email already exists. Choose a different one."})

        # Generate 4-digit OTP
        otp = random.randint(1000, 9999)

        # Send OTP to email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}. Do not share it with anyone.',
            'juicebarassist@gmail.com',  # Change to your email
            [email],
            fail_silently=False,
        )

        # Store user details and OTP in session
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'password': password1,
            'otp': otp
        }

        return redirect('otp_verification')  # Redirect to OTP verification page

    return render(request, 'signup.html')


def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data', {})

        if not signup_data:
            return redirect('signup')  # Redirect if session expired

        if str(signup_data['otp']) == entered_otp:
            # OTP is correct, save user
            user = CustomUser.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password']
            )
            user.save()

            # Clear session data
            del request.session['signup_data']

            return redirect('login')  # Redirect to login page

        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP. Try again.'})

    return render(request, 'otp_verification.html')

#Cloudinary 
def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

def gallery(request):
    images = ImageUpload.objects.all()
    return render(request, 'gallery.html', {'images': images})