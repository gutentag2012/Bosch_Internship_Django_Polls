from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Poll(models.Model):
    """A model that represents a collection with a collection of answers.
    It also contains two dates that represent the start and possible a end time.
    A poll can be identified through a collection of tags."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=240)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)

    def get_tags(self):
        """Retrieves the tags the poll is connected to as a collection of maps
        with the name and the color of the tag."""
        tags = []
        for tag in self.tag_set.all():
            tags.append({
                "name": tag.name,
                "color": tag.color % 15 + 1
            })
        return tags

    def count_votes(self):
        """Returns the number of votes on the poll."""
        return sum(map(lambda e: e.count_votes(), self.pollanswer_set.all()))

    def is_still_available(self):
        """Returns wether the polls time range contains the current date. So if the poll has
        still a valid date."""
        now = date.today()
        start_in_past = self.start_date <= now
        end_in_future = self.end_date is None or now <= self.end_date
        return start_in_past and end_in_future


class PollAnswer(models.Model):
    """A model that represents a specific answer to a poll. The number of votes
    on this answer is stored as a connection to the user that voted."""
    answer = models.TextField(max_length=240)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, null=True)

    def count_votes(self):
        """Returns the number of votes for this specific answer."""
        return self.users.all().count()


class Tag(models.Model):
    """A model that represents a specific category. It holds a connection to the polls described
    with this tag. It also has a color and name assiciated with it."""
    name = models.CharField(max_length=100)
    color = models.IntegerField()
    polls = models.ManyToManyField(Poll, blank=True, null=True)
