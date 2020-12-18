from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
from products.recommender import Recommender
from carts.forms import CartAddProductForm
from carts.carts import Cart
from utils.constants import KEY_OVERRIDE, KEY_QUANTITY
# Create your views here.


def product_list(request, category_slug=None):
    """ get list of products along with categories matching given category slug """

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'eShop/products/product_list.html', {
        'category': category, 'categories': categories, 'products': products})


def product_details(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id, translations__language_code=language,
                                translations__slug=slug, available=True)
    cart = Cart(request)
    current_product = cart.get_product(product)
    if current_product:
        cart_product_form = CartAddProductForm(initial={
            KEY_QUANTITY: current_product[KEY_QUANTITY], KEY_OVERRIDE: True
        })
    else:
        cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'eShop/products/product_details.html', {
        'product': product, 'cart_product_form': cart_product_form,
        'recommended_products': recommended_products
    })
