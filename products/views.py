from django.shortcuts import render, get_object_or_404
from products.models import Product, Category

# Create your views here.


def product_list(request, category_slug=None):
    """ get list of products along with categories matching given category slug """

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'eShop/products/product_list.html', {
        'category': category, 'categories': categories, 'products': products
    })


def product_details(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'eShop/products/product_details.html', {
        'product': product
    })
