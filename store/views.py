from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .filters import ProductFilter

# Create your views here.
def store(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    
    context = {
        'products': products,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'store/store.html', context)

def categories(request):

    all_categories = Category.objects.all()

    return {"all_categories" : all_categories}

def product_info(request,slug):

    product = get_object_or_404(Product,slug=slug)
    context = {"product":product}
    return render(request, 'store/product-info.html',context)


def list_category(request,slug):

    category = get_object_or_404(Category,slug=slug)
    products = Product.objects.filter(category=category)
    context = {"products":products,"category":category}
    return render(request, 'store/list-category.html',context)
