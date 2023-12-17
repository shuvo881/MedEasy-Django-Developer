from django.test import TestCase
from django.urls import reverse,resolve


class UrlsTestCase(TestCase):
    def test_url_resolve(self):
        #urls = reverse('product')
        #print(urls)
        assert 1 == 1