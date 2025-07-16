from django.contrib import admin
from shop.models import Order, Product

admin.site.register([Product, Order])
