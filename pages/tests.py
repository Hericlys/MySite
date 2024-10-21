from django.test import TestCase
from django.urls import reverse


class PagesURLsTest(TestCase):
    def test_pages_home_is_using_the_correct_url(self):
        home_url = reverse('pages:home')
        self.assertEqual(home_url, '/')
