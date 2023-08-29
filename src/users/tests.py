import urllib.parse
import json
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from uploads.views import home_view
from .views import login_view, register_view, logout_view
# Create your tests here.


class LoginSuccessful(TestCase):
    fixtures = ["testuser.json"]

    def test_login_get(self):
        response = self.client.get(path="/login/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_post(self):
        data = {"username": "test@test.com", "password": "nonnumericpassword1"}
        response1 = self.client.get(path=reverse(login_view))
        data["csrfmiddlewaretoken"] = response1.cookies["csrftoken"].value
        data = urllib.parse.urlencode(data)

        response2 = self.client.post(path=reverse(login_view),
                                     data=data,
                                     content_type="application/x-www-form-urlencoded",
                                     follow=True)
        self.assertRedirects(response2, expected_url=reverse(home_view))

class RegisterSuccesfful(TestCase):
    def test_register_get(self):
        response = self.client.get(path=reverse(register_view))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_post(self):
        data = {"email": "testdev@test.com", "password1": "nonnumericpassword1",
                "password2": "nonnumericpassword1"}
        response1 = self.client.get(path=reverse(register_view))
        data["csrfmiddlewaretoken"] = response1.cookies["csrftoken"].value
        data = urllib.parse.urlencode(data)
        response2 = self.client.post(path=reverse(register_view),
                                     data=data,
                                     content_type="application/x-www-form-urlencoded",
                                     follow=True)
        self.assertRedirects(response2, expected_url=reverse(login_view))

class LogoutSuccessful(TestCase):
    fixtures = ["testuser.json"]
    def setUp(self) -> None:
        data = {"username": "test@test.com", "password": "nonnumericpassword1"}
        response1 = self.client.get(path=reverse(login_view))
        data["csrfmiddlewaretoken"] = response1.cookies["csrftoken"].value
        data = urllib.parse.urlencode(data)

        response2 = self.client.post(path=reverse(login_view),
                                     data=data,
                                     content_type="application/x-www-form-urlencoded",
                                     follow=True)

    def test_logout_get(self):
        response = self.client.get(path=reverse(logout_view))
        self.assertRedirects(response, expected_url=reverse(login_view))

