from datetime import date
import uuid

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from base.querysets import VoucherQuerySet


class BaseModel(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    
    @classmethod
    def between(cls, start_date: date, end_date: date):
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
            if start_date > end_date: # just switch
                temp = start_date
                start_date = end_date
                end_date = temp
            
            return cls.objects.filter(created_at__date__gte=start_date, created_date__date__lte=end_date)
        
        elif start_date:
            return cls.objects.filter(created_at__date__gte=start_date)
        
        elif end_date:
            return cls.objects.filter(created_at__date__lte=end_date)
        
        else:
            return cls.objects.filter(created_at__date=timezone.now().date())
    
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
    
    total = models.PositiveIntegerField(default=0)
    number = models.CharField(max_length=32)
    paid = models.PositiveIntegerField(default=0)
    rest = models.PositiveIntegerField(default=0)
    with_debt = models.BooleanField(default=False)
    
    agent = models.ForeignKey(to=Agent, null=True, on_delete=models.SET_NULL)
    
    objects = VoucherQuerySet.as_manager()
    
    def calculate_rest(self):
        """
        It takes the total amount of the bill and subtracts the amount that has been paid
        :return: The difference between the total and the paid.
        """
        return self.total - self.paid
    
    def calculate_total(self):
        """
        It takes the value of the `paid` attribute and adds it to the value of the `rest` attribute, and
        returns the result
        :return: The total amount of money paid and the rest of the money owed.
        """
        return self.paid + self.rest
    
    @classmethod
    def profits(cls, queryset: VoucherQuerySet) -> int:
        """
        > It returns the total sum of all the vouchers in the queryset minus the total sum of the buy prices
        of all the details in the queryset
        
        :param cls: The class of the model that the manager is attached to
        :param queryset: The queryset of the model you want to get the total sum of
        :type queryset: QuerySet
        :return: The total sum of all the vouchers in the queryset.
        """
        
        total_sum = queryset.total_sum()
        buy_sum = sum([
            detail.buy_price for voucher in queryset for detail in voucher.details.all()
        ])
        
        return total_sum - buy_sum
    
    @classmethod
    def stats(cls, start_date, end_date):
        """
        It returns a dictionary with the total sum, the number of vouchers, the number of articles, the
        total quantity and the total rest sum of the queryset
        
        :param cls: The class of the model we're using
        :param start_date: The start date of the period to get the stats for
        :param end_date: The end date of the period
        :return: A dictionary with the keys: total_sum, vouchers_count, articles_count, quantity_sum,
        rest_sum
        """
        queryset : VoucherQuerySet = cls.between(start_date, end_date)
        
        return {
            "total_sum": queryset.total_sum(),
            "vouchers_count": queryset.vouchers_count(),
            "articles_count": queryset.articles_count(),
            "quantity_sum": queryset.quantity_sum(),
            "rest_sum": queryset.rest_sum(),
        }

    
    class Meta:
        abstract = True


class Transaction(BaseModel):
    from agents.models import Agent
    
    value = models.IntegerField()
    
    agent = models.ForeignKey(to=Agent, on_delete=models.DO_NOTHING)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_value = self.value
    
    @classmethod
    def value_between(cls, start_date, end_date) -> int:
        """
        > It returns the sum of the `value` field for all objects in the queryset that are between the
        `start_date` and `end_date` parameters
        
        :param cls: The class that the method is being called on
        :param start_date: The start date of the period
        :param end_date: The end date of the period
        :return: A dictionary with the key "value_sum" and the value of the sum of the values of the
        queryset.
        """
        
        queryset = cls.between(start_date, end_date)
        
        return queryset.aggregate(value_sum=Sum("value")).get("value_sum", 0)
    
    class Meta:
        abstract = True