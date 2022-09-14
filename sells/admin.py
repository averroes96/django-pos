from django.contrib import admin

from sells.models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "phone_first", "fax", "balance", "trade_registry" , "fiscal_id"]
    search_fields = ["__str__", "phone_first", "phone_second", "fax", "trade_registry", "fiscal_id"]
    list_per_page = 16