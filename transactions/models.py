from django.db import models

from base.models import BaseModel

from agents.models import Agent

from sells.models import Client

from buys.models import Supplier

# Create your models here.


class Transaction(BaseModel):
    value = models.IntegerField()
    agent = models.ForeignKey(to=Agent, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        abstract = True


class ClientTransaction(Transaction):
    client = models.ForeignKey(to=Client, null=True, on_delete=models.SET_NULL)


class SupplierTransaction(Transaction):
    supplier = models.ForeignKey(to=Supplier, null=True, on_delete=models.SET_NULL)


class Expense(BaseModel):
    
    class Types:
        EMPLOYEES = 1
    
    EXPENSE_TYPES = (
        (Types.EMPLOYEES, "employees"),
    )
    
    value = models.IntegerField()
    type = models.IntegerField(choices=EXPENSE_TYPES)
    note = models.TextField()
    
    agent = models.ForeignKey(to=Agent, null=True, on_delete=models.SET_NULL)
    
