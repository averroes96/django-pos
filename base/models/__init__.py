import uuid

from django.db import models



class BaseModel(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    
    class Meta:
        abstract = True
        get_latest_by = ['created_at']
        ordering = ['-created_at']

class Partner(BaseModel):
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    phone_first = models.CharField(max_length=16, null=True, blank=True)
    phone_second = models.CharField(max_length=16, null=True, blank=True)
    fax = models.CharField(max_length=16, null=True, blank=True)
    fiscal_id = models.CharField(max_length=16, null=True, blank=True)
    trade_registry = models.CharField(max_length=32, null=True, blank=True)
    balance = models.IntegerField(default=0)
    balance_initial = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        abstract = True
        get_latest_by = ['created_at']
        ordering = ['-created_at']


class Voucher(BaseModel):
    from agents.models import Agent
    
    def calculate_rest(self):
        return self.total - self.paid
    
    def calculate_total(self):
        return self.paid + self.rest
    
    total = models.PositiveIntegerField(default=0)
    number = models.CharField(max_length=32)
    paid = models.PositiveIntegerField(default=0)
    rest = models.PositiveIntegerField(default=0)
    with_debt = models.BooleanField(default=False)
    
    agent = models.ForeignKey(to=Agent, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True