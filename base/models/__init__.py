from datetime import date
import uuid

from django.db import models
from django.db.models import Sum, Count, QuerySet
from django.utils import timezone



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
    
    total = models.PositiveIntegerField(default=0)
    number = models.CharField(max_length=32)
    paid = models.PositiveIntegerField(default=0)
    rest = models.PositiveIntegerField(default=0)
    with_debt = models.BooleanField(default=False)
    
    agent = models.ForeignKey(to=Agent, null=True, on_delete=models.SET_NULL)
    
    @classmethod
    def profits(cls, queryset: QuerySet) -> int:
        """
        > It returns the total sum of the queryset minus the sum of the buy prices of all the articles in
        the queryset
        
        :param cls: The class of the model that the manager is attached to
        :param queryset: The queryset to be used for the calculation
        :type queryset: QuerySet
        :return: A dictionary with the key "profit" and the value of the profit.
        """
        
        total_sum = cls.total_sum(queryset)
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
        queryset = cls.between(start_date, end_date)
        
        return {
            "total_sum": cls.total_sum(queryset),
            "vouchers_count": cls.vouchers_count(queryset),
            "articles_count": cls.articles_count(queryset),
            "quantity_sum": cls.quantity_sum(queryset),
            "rest_sum": cls.rest_sum(queryset),
        }
    
    @classmethod
    def total_sum(cls, queryset: QuerySet):
        """
        > It returns the total sum of the queryset
        
        :param cls: The class of the model that the queryset is for
        :param queryset: The queryset to be used to calculate the total sum
        :type queryset: QuerySet
        :return: A dictionary with the key "total_sum" and the value of the sum of the total field.
        """
        
        total_sum = queryset.aggregate(total_sum=Sum("total")).get("total_sum")
        
        return total_sum if total_sum else 0
    
    @classmethod
    def vouchers_count(cls, queryset: QuerySet):
        """
        > It returns the number of vouchers in a queryset
        
        :param cls: The class of the model that the queryset is for
        :param queryset: The queryset to be used to calculate the count
        :type queryset: QuerySet
        :return: A dictionary with the key "vouchers_count" and the value of the count of the queryset.
        """
        
        return queryset.aggregate(vouchers_count=Count("id")).get("vouchers_count", 0)

    @classmethod
    def articles_count(cls, queryset: QuerySet):
        """
        > It returns the number of articles in a queryset
        
        :param cls: The class of the model that the queryset is for
        :param queryset: The queryset to be annotated
        :type queryset: QuerySet
        :return: A dictionary with the key "articles_count" and the value of the count of the articles.
        """
        
        return queryset.aggregate(
            articles_count=Count("details__article", distinct=True)
        ).get("articles_count", 0)

    @classmethod
    def quantity_sum(cls, queryset: QuerySet):
        """
        > It returns the sum of the quantity of all the details of the queryset
        
        :param cls: The class of the model that the queryset is for
        :param queryset: The queryset to be used for the aggregation
        :type queryset: QuerySet
        :return: A dictionary with the key "quantity_sum" and the value of the sum of the quantity of all
        the details of the queryset.
        """
        
        return queryset.aggregate(quantity_sum=Count("details__quantity")).get("quantity_sum", 0)
    
    @classmethod
    def rest_sum(cls, queryset: QuerySet) -> int:
        """
        > It returns the sum of the `rest` field of a queryset
        
        :param cls: the class of the model
        :param queryset: The queryset to be filtered
        :type queryset: QuerySet
        :return: A QuerySet object.
        """
        
        rest_sum = queryset.aggregate(rest_sum=Sum("rest")).get("rest_sum")
        
        return rest_sum if rest_sum else 0   

    
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