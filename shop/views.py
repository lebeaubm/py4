from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

def homepage(request):
    return render(request, 'shop/homepage.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'shop/login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def profile(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_count = cart_items.count()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/profile.html', {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
        'total_price': total_price
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        Order.objects.create(user=request.user, product=item.product, quantity=item.quantity)
        item.delete()
    return redirect('profile')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required(login_url='register')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
