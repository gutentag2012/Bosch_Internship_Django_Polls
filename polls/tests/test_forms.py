from django.test import TestCase
from polls.forms import PollForm
from django.contrib.auth.models import User


class PollFormTestCase(TestCase):

    def test_valid_data(self):
        user = User.objects.create_user(username="username", password="password")
        form = PollForm(data={
            "creator": user,
            "question": "This is the question?",
            "start_date": "Mar 12, 2021",
            "answer_1": "First Answer",
            "answer_2": "Second Answer",
            "answer_3": "Third Answer"
        })
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = PollForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_wrong_end_date(self):
        user = User.objects.create_user(username="username", password="password")
        form = PollForm(data={
            "creator": user,
            "question": "This is the question?",
            "start_date": "Mar 12, 2021",
            "end_date": "Mar 10, 2021",
            "answer_1": "First Answer",
            "answer_2": "Second Answer",
            "answer_3": "Third Answer"
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
