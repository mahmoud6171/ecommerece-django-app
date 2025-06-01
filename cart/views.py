from django.shortcuts import render, redirect
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.

def cart_summary(request):
    return render(request, 'cart/cart-summary.html')

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
            cart.add(product=product, product_qty=product_qty)
            messages.success(request, f"{product.title} added to cart successfully!")
        except Product.DoesNotExist:
            messages.error(request, "Product not found!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('store')


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            cart.delete(product=product_id)
            messages.success(request, f"{product.title} removed from cart successfully!")
        except Product.DoesNotExist:
            messages.error(request, "Product not found!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('store')


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_quantity'))
        
        try:
            product = Product.objects.get(id=product_id)
            cart.update(product=product_id, qty=product_qty)
            messages.success(request, f"Cart updated for {product.title}!")
        except Product.DoesNotExist:
            messages.error(request, "Product not found!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return redirect('store')

