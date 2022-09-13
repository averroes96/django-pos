from django.contrib import admin

from buys.models import Supplier

# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "phone_first", "fax", "balance", "trade_registry" , "fiscal_id"]
    search_fields = ["__str__", "phone_first", "phone_second", "fax", "trade_registry", "fiscal_id"]
    list_per_page = 16

