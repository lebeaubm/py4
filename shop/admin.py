from django.contrib import admin
from .models import Product, Order, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'ordered_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('ordered_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)

