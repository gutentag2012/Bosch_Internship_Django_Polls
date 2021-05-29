from django.test import SimpleTestCase
from django.urls import reverse, resolve
from polls import views


class PollsUrlsTestCase(SimpleTestCase):

    def simple_url_test(self, url_text, view_func):
        url = reverse(url_text)
        self.assertEqual(resolve(url).func, view_func)

    def test_home_is_resolved(self):
        self.simple_url_test("home", views.home_page_view)

    def test_login_is_resolved(self):
        self.simple_url_test("login", views.log_in_view)

    def test_signup_is_resolved(self):
        self.simple_url_test("signup", views.sign_up_view)

    def test_create_poll_is_resolved(self):
        self.simple_url_test("create-poll", views.create_poll_view)

    def test_single_poll_is_resolved(self):
        url = reverse("polls", args=[1])
        self.assertEqual(resolve(url).func, views.single_poll_view)

    def test_delete_poll_is_resolved(self):
        url = reverse("delete-poll", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.PollDeleteView)
