from django.test import TestCase, Client
from django.urls import reverse
from polls.models import Poll, PollAnswer, Tag
from django.contrib.auth.models import User
from datetime import date
import json


class PollsViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="Username", password="password")
        self.poll = Poll.objects.create(creator=self.user, question="Question", start_date=date.today())

    def simple_GET_response_test(self, response, template):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def simple_GET_test(self, url, template):
        response = self.client.get(reverse(url))
        self.simple_GET_response_test(response, template)

    def test_login_GET(self):
        self.simple_GET_test("login", "login.html")

    def test_signup_GET(self):
        self.simple_GET_test("signup", "signup.html")

    def test_home_GET(self):
        self.simple_GET_test("home", "overview_polls.html")

    def test_create_GET(self):
        self.simple_GET_test("create-poll", "create_poll.html")

    def test_single_poll_GET(self):
        response = self.client.get(reverse("polls", args=[1]))
        self.simple_GET_response_test(response, "single_poll.html")

    def test_delete_GET(self):
        response = self.client.get(reverse("delete-poll", args=[1]))
        self.simple_GET_response_test(response, "delete_poll.html")

    def test_login_POST(self):
        pass
