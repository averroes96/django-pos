from stats.views import BuyStatsView, SellStatsView, ReportStatsView

from django.urls import path

urlpatterns = [
    path("buys/", BuyStatsView.as_view(), name="buy-stats"),
    path("sells/", SellStatsView.as_view(), name="sell-stats"),
    path("report/", ReportStatsView.as_view(), name="report-stats")
]