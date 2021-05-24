from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=240)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)


class PollAnswer(models.Model):
    answer = models.TextField(max_length=240)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=24)
    polls = models.ManyToManyField(Poll)
