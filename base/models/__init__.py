import uuid

from django.db import models
from django.db.models import Sum, Count
from django.utils import timezone



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
    
    @classmethod
    def stats(cls, start_date, end_date):
        """
        > It returns a dictionary with the total sum of all the orders, the number of orders, the number of
        different articles, the total quantity of articles and the total sum of the rest of the orders
        
        :param cls: The class that the method is being called on
        :param start_date: The start date of the period to filter by
        :param end_date: The end date of the period
        """
        return cls.between(start_date, end_date).aggregate(
            total_sum=Sum("total"), 
            buys_count=Count("id"),
            articles_count=Count("details__article", distinct=True),
            quantity_sum=Sum("details__quantity"),
            rest_sum=Sum("rest")
        )
    
    @classmethod
    def between(cls, start_date, end_date):
        """
        If the start date and end date are both present, return all the objects that were created between
        the start date and end date. If only the start date is present, return all the objects that were
        created after the start date. If only the end date is present, return all the objects that were
        created before the end date. If neither the start date nor the end date are present, return all the
        objects that were created today
        
        :param cls: This is the class that the method is being called on. In this case, it's the Voucher class
        :param start_date: The start date of the range
        :param end_date: The end date of the range
        :return: A list of all the objects in the database that have a created_at date that is greater than
        or equal to the start_date and less than or equal to the end_date.
        """
        
        if start_date and end_date:
            return cls.objects.filter(created_at__date__gte=start_date, created_date__date__lte=end_date)
        elif start_date:
            return cls.objects.filter(created_at__date__gte=start_date)
        elif end_date:
            return cls.objects.filter(created_at__date__lte=end_date)
        else:
            return cls.objects.filter(created_at__date=timezone.now().date())
    
    class Meta:
        abstract = True