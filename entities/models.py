from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=240)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)

    def get_tags(self):
        tags = []
        for tag in self.tag_set.all():
            tags.append({
                "name": tag.name,
                "color": tag.color % 15 + 1
            })
        return tags

    def count_votes(self):
        return sum(map(lambda e: e.count_votes(), self.pollanswer_set.all()))


class PollAnswer(models.Model):
    answer = models.TextField(max_length=240)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, null=True)

    def count_votes(self):
        return self.users.all().count()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.IntegerField()
    polls = models.ManyToManyField(Poll, blank=True, null=True)
