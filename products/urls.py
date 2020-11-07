from django.urls import path
from products.views import product_list, product_details

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:id>/<slug:slug>/', product_details, name='product_details'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
]
