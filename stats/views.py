from rest_framework.views import APIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser

from buys.models import BuyVoucher

from sells.models import SellVoucher

# Create your views here.


class BuyStatsView(APIView):
    
    permission_classes = [IsAdminUser]
    
    def get(self, request: HttpRequest):
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        stats = BuyVoucher.stats(start_date, end_date)
        
        if not stats.get("buys_count"):
            return Response({
                "total_sum": 0,
                "buys_count": 0,
                "articles_count": 0,
                "quantity_sum": 0,
                "rest_sum": 0,
            })
        
        return Response(stats)


class SellStatsView(APIView):
    
    permission_classes = [IsAdminUser]
    
    def get(self, request: HttpRequest):
        
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        
        stats = SellVoucher.stats(start_date, end_date)
        
        print(stats)
        
        if not stats.get("buys_count"):
            return Response({
                "total_sum": 0,
                "buys_count": 0,
                "articles_count": 0,
                "quantity_sum": 0,
                "rest_sum": 0,
            })
        
        return Response(stats)