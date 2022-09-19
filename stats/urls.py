from stats.views import BuyStatsView

from django.urls import path

urlpatterns = [
    path("buys/", BuyStatsView.as_view(), name="buy-stats")
]