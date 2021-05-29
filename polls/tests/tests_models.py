from django.test import TestCase
from django.contrib.auth.models import User
from polls.models import Poll, PollAnswer, Tag
from datetime import date, timedelta


class BaseModelTest(TestCase):
    today = date.today()
    theDayBefore = date.today() - timedelta(days=1)
    theDayAfter = date.today() + timedelta(days=1)
    twoDaysBefore = date.today() - timedelta(days=2)
    twoDaysAfter = date.today() + timedelta(days=2)

    def setUp(self):
        self.user_1 = User.objects.create(username="Username 1", password="Password")
        self.user_2 = User.objects.create(username="Username 2", password="Password")
        self.user_3 = User.objects.create(username="Username 3", password="Password")
        self.user_4 = User.objects.create(username="Username 4", password="Password")
        self.poll_with_relations = Poll.objects.create(creator=self.user_1, question="Relations", start_date=self.today)
        self.poll_answer_1 = PollAnswer.objects.create(poll=self.poll_with_relations, answer="Answer 1")
        self.poll_answer_2 = PollAnswer.objects.create(poll=self.poll_with_relations, answer="Answer 2")
        self.poll_answer_3 = PollAnswer.objects.create(poll=self.poll_with_relations, answer="Answer 3")
        self.poll_answer_4 = PollAnswer.objects.create(poll=self.poll_with_relations, answer="Answer 4")
        self.poll_tag_1 = Tag.objects.create(name="Tag 1", color=1)
        self.poll_tag_2 = Tag.objects.create(name="Tag 2", color=1)
        self.poll_tag_3 = Tag.objects.create(name="Tag 3", color=1)
        self.poll_tag_4 = Tag.objects.create(name="Tag 4", color=1)
        self.poll_with_relations.pollanswer_set.add(self.poll_answer_1)
        self.poll_with_relations.pollanswer_set.add(self.poll_answer_2)
        self.poll_with_relations.pollanswer_set.add(self.poll_answer_3)
        self.poll_with_relations.tag_set.add(self.poll_tag_1)
        self.poll_with_relations.tag_set.add(self.poll_tag_2)
        self.poll_with_relations.tag_set.add(self.poll_tag_3)
        self.poll_answer_1.user_votes.add(self.user_1)
        self.poll_answer_1.user_votes.add(self.user_2)
        self.poll_answer_2.user_votes.add(self.user_1)
        self.poll_answer_2.user_votes.add(self.user_2)
        self.poll_answer_2.user_votes.add(self.user_3)
        self.poll_answer_3.user_votes.add(self.user_1)


class PollModelTests(BaseModelTest):

    def test_is_still_available(self):
        """Check if the timespan of a poll contains the current date"""
        p = Poll(question="Question", start_date=self.theDayBefore, end_date=self.today)
        p1 = Poll(question="Question", start_date=self.theDayBefore, end_date=self.theDayAfter)
        p2 = Poll(question="Question", start_date=self.today, end_date=self.theDayAfter)
        p3 = Poll(question="Question", start_date=self.theDayAfter, end_date=self.twoDaysAfter)
        p4 = Poll(question="Question", start_date=self.twoDaysBefore, end_date=self.theDayBefore)

        self.assertTrue(p.is_still_available())
        self.assertTrue(p1.is_still_available())
        self.assertTrue(p2.is_still_available())
        self.assertFalse(p3.is_still_available())
        self.assertFalse(p4.is_still_available())

    def test_get_tags(self):
        """Checks if the tags are converted correctly into a dictionary"""
        tags = self.poll_with_relations.get_tags()

        self.assertIn({"name": self.poll_tag_1.name, "color": self.poll_tag_1.color % 15 + 1}, tags)
        self.assertIn({"name": self.poll_tag_2.name, "color": self.poll_tag_2.color % 15 + 1}, tags)
        self.assertIn({"name": self.poll_tag_3.name, "color": self.poll_tag_3.color % 15 + 1}, tags)
        self.assertNotIn({"name": self.poll_tag_4.name, "color": self.poll_tag_4.color % 15 + 1}, tags)

    def test_count_votes(self):
        """Check whether the votes in the poll are counted correctly"""
        self.assertIs(self.poll_with_relations.count_votes(), 6)


class PollAnswerModelTests(BaseModelTest):

    def test_count_votes(self):
        """Check whether the votes in the poll are counted correctly"""
        self.assertIs(self.poll_answer_1.count_votes(), 2)
        self.poll_answer_1.user_votes.add(self.user_3)
        self.assertIs(self.poll_answer_1.count_votes(), 3)
