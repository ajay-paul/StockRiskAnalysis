from django.urls import path
from .views import StockPredictionView

urlpatterns = [
    path('risk/<str:symbol>/', StockPredictionView.as_view(), name='risk-analysis'),
]
