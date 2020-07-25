from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

class Stock(models.Model):
    BID = models.IntegerField()
    BIDVOL = models.FloatField()
    CUR = models.FloatField()
    HIGH = models.FloatField()
    LOW = models.FloatField()
    MCAP = models.TextField()
    TRND = models.CharField(max_length=10)
    last_modified_string = models.CharField(max_length=200)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    created_on = models.DateField(default=timezone.now)