from django.contrib import admin

# Register your models here.
from auction.models import Customer, Item, Bid


class ItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'price', 'start_date', 'end_date', 'image','comments','customer_id')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'mobile_num','street_address','city','state','zipcode')




class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'time', 'item_id','customer_id')


admin.site.register(Customer,CustomerAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Bid,BidAdmin)
