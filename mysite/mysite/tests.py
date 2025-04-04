from django.test import TestCase, Client
from django.urls import reverse

class HomePageTest(TestCase):
    def test_home_page_returns_correct_response(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, AWS Elastic Beanstalk!")
