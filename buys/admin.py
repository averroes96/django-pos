from django.contrib import admin

from buys.models import Supplier, BuyVoucher, BuyVoucherDetail

# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "phone_first", "fax", "balance", "trade_registry" , "fiscal_id"]
    search_fields = ["__str__", "phone_first", "phone_second", "fax", "trade_registry", "fiscal_id"]
    list_per_page = 16


@admin.register(BuyVoucher)
class BuyVoucherAdmin(admin.ModelAdmin):
    
    list_display = ["number", "total", "paid", "rest", "with_debt" , "supplier"]
    search_fields = ["number"]
    list_filter = ["with_debt", "supplier"]
    list_per_page = 16


@admin.register(BuyVoucherDetail)
class BuyVoucherDetailAdmin(admin.ModelAdmin):
    
    list_display = ["voucher", "article", "buy_price", "quantity"]
    list_filter = ["voucher", "article"]
    list_per_page = 16

