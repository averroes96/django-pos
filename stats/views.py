from rest_framework.views import APIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from stats.permissions import StatsPermission

from buys.models import BuyVoucher

from sells.models import SellVoucher

from pos.models import SaleVoucher

from transactions.models import Expense, ClientTransaction, SupplierTransaction

# Create your views here.


class BuyStatsView(APIView):
    
    permission_classes = [StatsPermission]
    
    def get(self, request: HttpRequest):
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        stats = BuyVoucher.stats(start_date, end_date)
        
        return Response(stats)


class SellStatsView(APIView):
    
    permission_classes = [StatsPermission]
    
    def get(self, request: HttpRequest):
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        stats = SellVoucher.stats(start_date, end_date)
        
        return Response(stats)


class ReportStatsView(APIView):
    
    permission_classes = [StatsPermission]
    
    def get(self, request: HttpRequest):
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        sells_queryset = SellVoucher.between(start_date, end_date)
        sales_queryset = SaleVoucher.between(start_date, end_date)
        
        sells_sum = SellVoucher.total_sum(queryset=sells_queryset)
        sales_sum = SaleVoucher.total_sum(queryset=sales_queryset)
        
        sells_profits = SellVoucher.profits(queryset=sells_queryset)
        sales_profits = SaleVoucher.profits(queryset=sales_queryset)
        
        sum = sales_sum + sells_sum
        profits = sells_profits + sales_profits
        expenses = Expense.value_between(start_date, end_date)
        client_transactions_sum = ClientTransaction.value_between(start_date, end_date)
        supplier_transactions_sum = SupplierTransaction.value_between(start_date, end_date)
        
        return Response({
            "sum": sum,
            "profits": profits,
            "expenses": expenses,
            "client_transactions_sum": client_transactions_sum,
            "supplier_transactions_sum": supplier_transactions_sum,
        })
        
        