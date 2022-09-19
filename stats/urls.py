from stats.views import BuyStatsView, SellStatsView

from django.urls import path

urlpatterns = [
    path("buys/", BuyStatsView.as_view(), name="buy-stats"),
    path("sells/", SellStatsView.as_view(), name="sell-stats")
]