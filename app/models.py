from djongo import models
from djongo import models as djongo_models


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    bitcoin_balance = models.FloatField()
    dollars_balance = models.FloatField()



class Order(models.Model):
    TYPE_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    quantity = models.FloatField()
    price = models.FloatField()
    executed = models.BooleanField(default=False)    



class Trade(djongo_models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    price = models.FloatField()
    quantity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)    