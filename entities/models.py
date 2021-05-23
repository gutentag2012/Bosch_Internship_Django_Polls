from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=240)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)
