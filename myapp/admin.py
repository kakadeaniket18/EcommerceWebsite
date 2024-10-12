from django.contrib import admin
from myapp.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','pdetails','is_active']
    list_filter=['cat','is_active']

admin.site.register(Product,ProductAdmin)