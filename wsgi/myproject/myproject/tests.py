from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import requests

class RequestsTestCase(StaticLiveServerTestCase):
    """
    A base test case for Requests when running live server test case
    """

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def open(self, url):
        return requests.get("%s%s" % (self.live_server_url, url))

class StaticFilesTestCase(RequestsTestCase):
    '''
     django.test.client doesn't find static files when just using
     TestCase and Client
    '''
    test_url = '/static/js/test.js'

    def test_static_file_get(self):
        r= self.open(self.test_url+'wrong')
        self.assertTrue(r.status_code != 200)
        r= self.open(self.test_url)
        self.assertTrue(r.status_code == 200)
