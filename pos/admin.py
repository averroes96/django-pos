from django.contrib import admin

from pos.models import SaleVoucher, SaleVoucherDetail

# Register your models here.


@admin.register(SaleVoucher)
class SaleVoucherAdmin(admin.ModelAdmin):
    
    list_display = ["number", "total", "paid", "rest", "with_debt" , "client"]
    search_fields = ["number"]
    list_filter = ["with_debt", "client"]
    list_per_page = 16


@admin.register(SaleVoucherDetail)
class SaleVoucherDetailAdmin(admin.ModelAdmin):
    
    list_display = ["voucher", "article", "sell_price", "buy_price", "quantity"]
    list_filter = ["voucher", "article"]
    list_per_page = 16
