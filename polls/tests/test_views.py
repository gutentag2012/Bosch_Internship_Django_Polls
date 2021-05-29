from django.test import TestCase, Client
from django.urls import reverse
from polls.models import Poll, PollAnswer, Tag
from django.contrib.auth.models import User
from datetime import date
import json


class BaseViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Username", password="password")
        self.poll = Poll.objects.create(creator=self.user, question="Question", start_date=date.today())
        self.answer = PollAnswer.objects.create(poll=self.poll, answer="Answer")

    def simple_GET_response_test(self, response, template):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def simple_GET_test(self, url, template):
        response = self.client.get(reverse(url))
        self.simple_GET_response_test(response, template)
        return response

    def login(self):
        return self.client.post(reverse("login"), {
            "username": "Username",
            "password": "password",
        })


class LoginViewTestCase(BaseViewsTestCase):

    def test_login_GET(self):
        self.simple_GET_test("login", "login.html")

    def test_login_POST(self):
        response = self.login()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.wsgi_request.user, self.user)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_POST_invalid(self):
        response = self.client.post(reverse("login"), {
            "username": "Username123",
            "password": "password"
        })
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["is_error"])
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignupViewTestCase(BaseViewsTestCase):

    def test_signup_GET(self):
        self.simple_GET_test("signup", "signup.html")

    def test_sigup_POST(self):
        response = self.client.post(reverse("signup"), {
            "username": "Username123",
            "password1": "password312123",
            "password2": "password312123"
        })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEquals(User.objects.count(), 2)

    def test_sigup_POST_invalid(self):
        response = self.client.post(reverse("signup"), {
            "username": "Username123",
            "password1": "password",
            "password2": "password312123"
        })
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEquals(User.objects.count(), 1)


class HomeViewTestCase(BaseViewsTestCase):

    def test_home_GET(self):
        response = self.simple_GET_test("home", "overview_polls.html")
        self.assertEquals(len(response.context["polls"]), 1)

    def test_home_search_GET(self):
        response = self.client.get(reverse("home"), {
            "search": "asdasdasd"
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context["polls"]), 0)


class SingleViewTestCase(BaseViewsTestCase):

    def test_single_poll_GET(self):
        response = self.client.get(reverse("polls", args=[1]))
        self.simple_GET_response_test(response, "single_poll.html")

    def test_single_poll_GET_invalid(self):
        response = self.client.get(reverse("polls", args=[2]))
        self.assertEquals(response.status_code, 404)

    def test_single_poll_vote_POST_unauthorized(self):
        response = self.client.post(reverse("polls", args=[1]), {
            "vote": 1
        })
        self.simple_GET_response_test(response, "single_poll.html")
        self.assertEquals(self.poll.count_votes(), 0)
        self.assertTrue(response.context["is_error"])

    def test_single_poll_vote_POST(self):
        self.login()
        response = self.client.post(reverse("polls", args=[1]), {
            "vote": 1
        })
        self.simple_GET_response_test(response, "single_poll.html")
        self.assertEquals(self.poll.count_votes(), 1)
        self.client.post(reverse("polls", args=[1]), {
            "vote": 1
        })
        self.assertEquals(self.poll.count_votes(), 1)

    def test_single_poll_vote_POST_invalid(self):
        self.client.login()
        response = self.client.post(reverse("polls", args=[1]), {
            "vote": 2
        })
        self.simple_GET_response_test(response, "single_poll.html")
        self.assertEquals(self.poll.count_votes(), 0)


class DeleteViewTestCase(BaseViewsTestCase):

    def test_delete_GET(self):
        self.login()
        response = self.client.get(reverse("delete-poll", args=[1]))
        self.simple_GET_response_test(response, "delete_poll.html")

    def test_delete_GET_unauthorized(self):
        response = self.client.get(reverse("delete-poll", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_delete_GET_invalid(self):
        self.login()
        response = self.client.get(reverse("delete-poll", args=[2]))
        self.assertEquals(response.status_code, 404)

    def test_delete_POST_unauthorited(self):
        response = self.client.post(reverse("delete-poll", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Poll.objects.count(), 1)

    def test_delete_POST(self):
        self.login()
        response = self.client.post(reverse("delete-poll", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Poll.objects.count(), 0)


class CreateViewTestCase(BaseViewsTestCase):

    def test_create_GET(self):
        self.login()
        self.simple_GET_test("create-poll", "create_poll.html")

    def test_create_GET_unauthorized(self):
        request = self.simple_GET_test("create-poll", "create_poll.html")
        self.assertTrue(request.context["is_error"])

    def test_create_POST(self):
        self.login()
        response = self.client.post(reverse("create-poll"), {
            "creator": 1,
            "question": "Question",
            "start_date": "Mar 12, 2021",
            "chip-2": "This is a tag",
            "chip-4": "This is another tag",
            "answer_1": "First required answer",
            "answer_2": "Second required answer",
            "answer_3": "Third required answer",
            "answer_4": "Fourth optional answer",
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Poll.objects.count(), 2)
        self.assertEquals(PollAnswer.objects.count(), 5)
        self.assertEquals(Tag.objects.count(), 2)

    def test_create_POST_invalid_1(self):
        self.login()
        response = self.client.post(reverse("create-poll"), {
            "creator": 1,
            "question": "Question",
            "start_date": "Mar 12, 2021",
            "chip-2": "This is a tag",
            "chip-4": "This is another tag",
            "answer_1": "First required answer",
            "answer_2": "Second required answer",
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Poll.objects.count(), 1)

    def test_create_POST_invalid_2(self):
        self.login()
        response = self.client.post(reverse("create-poll"), {
            "creator": 1,
            "question": "Question",
            "start_date": "Mar 12, 2021",
            "end_date": "Mar 10, 2021",
            "chip-2": "This is a tag",
            "chip-4": "This is another tag",
            "answer_1": "First required answer",
            "answer_2": "Second required answer",
            "answer_3": "Second required answer",
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Poll.objects.count(), 1)
