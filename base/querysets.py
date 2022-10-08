from django.db.models import QuerySet, Sum, Count


class VoucherQuerySet(QuerySet):
    
    def rest_sum(self) -> int:
        """
        It returns the sum of the rest attribute of all the objects in the model.
        :return: The sum of the rest field for all the objects in the queryset.
        """
        
        rest_sum = self.aggregate(rest_sum=Sum("rest")).get("rest_sum")
        
        return rest_sum if rest_sum else 0

    def quantity_sum(self):
        """
        "Return the sum of the quantity field for all the details associated with this order."
        
        :return: The quantity_sum is being returned.
        """
        
        return self.aggregate(quantity_sum=Count("details__quantity")).get("quantity_sum", 0)  

    def articles_count(self):
        return self.aggregate(
            articles_count=Count("details__article", distinct=True)
        ).get("articles_count", 0)

    def vouchers_count(self):
        return self.aggregate(vouchers_count=Count("id")).get("vouchers_count", 0)

    def total_sum(self):
        total_sum = self.aggregate(total_sum=Sum("total")).get("total_sum")
        
        return total_sum if total_sum else 0