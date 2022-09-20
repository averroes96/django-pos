from django.contrib import admin

from sells.models import Client, SellVoucher, SellVoucherDetail

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "phone_first", "fax", "balance", "trade_registry" , "fiscal_id"]
    search_fields = ["__str__", "phone_first", "phone_second", "fax", "trade_registry", "fiscal_id"]
    list_per_page = 16


@admin.register(SellVoucher)
class SellVoucherAdmin(admin.ModelAdmin):
    
    list_display = ["number", "total", "paid", "rest", "with_debt" , "client"]
    search_fields = ["number"]
    list_filter = ["with_debt", "client"]
    list_per_page = 16


@admin.register(SellVoucherDetail)
class SellVoucherDetailAdmin(admin.ModelAdmin):
    
    list_display = ["voucher", "article", "price", "quantity"]
    list_filter = ["voucher", "article"]
    list_per_page = 16