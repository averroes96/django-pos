from django.contrib import admin

from transactions.models import ClientTransaction, SupplierTransaction, Expense

# Register your models here.


@admin.register(ClientTransaction)
class ClientTransactionAdmin(admin.ModelAdmin):
    
    list_display = ["client", "value", "created_at", "agent"]
    list_filter = ["client", "agent"]
    list_per_page = 16


@admin.register(SupplierTransaction)
class SupplierTransactionAdmin(admin.ModelAdmin):
    
    list_display = ["supplier", "value", "created_at", "agent"]
    list_filter = ["supplier", "agent"]
    list_per_page = 16


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    
    list_display = ["type", "value", "created_at", "agent"]
    list_filter = ["type", "agent"]
    list_per_page = 16