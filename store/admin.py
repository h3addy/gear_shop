from store.models import Customer, Order, OrderItem, Product, ProductCategory, ShippigAddress
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippigAddress)
