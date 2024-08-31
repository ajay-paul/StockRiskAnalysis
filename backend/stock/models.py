from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.symbol} on {self.date}"

class StockPrediction(models.Model):
    stock = models.ForeignKey(StockData, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    actual_price = models.FloatField(null=True, blank=True)
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.stock.symbol} on {self.prediction_date}"
