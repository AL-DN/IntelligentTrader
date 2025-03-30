from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=4)
    date_created = models.DateTimeField(default=timezone.now)
    fin_rep_score = models.FloatField(null=True)

    def __str__(self):
        return self.ticker
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
class TickerData(models.Model):
    ticker = models.CharField(max_length=4, unique=True) # no need to store multiple instance of same ticker data
    dataset = models.JSONField()
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ticker
    
    def is_stale(self):
        return (timezone.now() - self.last_updated).days >= 1
    
    def to_DataFrame(self):
        import pandas as pd
        return pd.DataFrame(self.dataset)