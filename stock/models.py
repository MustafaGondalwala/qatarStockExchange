from django.db import models
from django.utils import timezone

# Create your models here.

class Stock(models.Model):
    BID = models.IntegerField()
    BIDVOL = models.FloatField()
    CUR = models.FloatField()
    HIGH = models.FloatField()
    LOW = models.FloatField()
    MCAP = models.TextField()
    TRND = models.CharField(max_length=10)
    created_on = models.DateTimeField(default=timezone.now)