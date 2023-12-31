from django.contrib import admin
from store.models import Cart, Product, Order, Goodie

# Register your models here.

admin.site.register(Product)
admin.site.register(Goodie)
admin.site.register(Order)
admin.site.register(Cart)
