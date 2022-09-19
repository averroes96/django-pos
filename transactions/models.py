from django.db import models

from base.models import Transaction

from sells.models import Client

from buys.models import Supplier

# Create your models here.


class ClientTransaction(Transaction):
    
    client = models.ForeignKey(to=Client, on_delete=models.DO_NOTHING)


class SupplierTransaction(Transaction):
    
    supplier = models.ForeignKey(to=Supplier, on_delete=models.DO_NOTHING)


class Expense(Transaction):
    
    class Types:
        EMPLOYEES = 1
    
    EXPENSE_TYPES = (
        (Types.EMPLOYEES, "employees"),
    )
    
    type = models.IntegerField(choices=EXPENSE_TYPES)
    note = models.TextField()
    
    
