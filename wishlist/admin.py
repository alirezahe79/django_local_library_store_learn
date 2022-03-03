from django.contrib import admin
from .models import WishList


# Register your models here.
class WishList_field(admin.ModelAdmin):
    fieldsets = [
        ('Infomation Wishlist:', {'fields': ['id_product', 'id_user', 'count']}),
        ('prices:', {'fields': ['total_price', 'unit_price', 'controler']}),
    ]
    list_display = ['id_product', 'id_user']
    search_fields = ['id_product']


admin.site.register(WishList, WishList_field)