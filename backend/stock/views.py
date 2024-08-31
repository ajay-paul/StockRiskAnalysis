from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, StockPrediction
from .serializers import StockPredictionSerializer
from .tasks import fetch_stock_data

class StockPredictionView(APIView):
    def get(self, request, symbol):
        stock = Stock.objects.get(symbol=symbol)
        predictions = StockPrediction.objects.filter(stock=stock)
        serializer = StockPredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def post(self, request):
        symbol = request.data.get('symbol')
        fetch_stock_data.delay(symbol)
        return Response({"message": "Stock data fetching initiated."}, status=status.HTTP_200_OK)
