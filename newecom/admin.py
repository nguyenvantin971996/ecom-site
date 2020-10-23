from django.contrib import admin
from .models import Customer,Product,Order,OrderItem,ShippingAddress,Comment
# Register your models here.
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','order']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','customer']

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Comment,CommentAdmin)