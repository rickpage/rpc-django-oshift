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

class GroupPermissionsTests(StaticLiveServerTestCase):
    """Should test that:

    Admins can change users
    Admins can delete users
    Moderators can change users
    Moderators cannot delete users
    regular users with no groups cannot change, or delete users
    TODO: regular users cannot view-users

    Do this by creating fixture data that includes an Admin, a Mod
    , and a regular user. The regular user can try to change to mod
    , etc
    """

    def setUp(self):
        pass

    def test_admin_change_user(self):
        pass

    def test_admin_delete_user(self):
        pass

    def test_mod_change_user(self):
        pass

    def test_mod_delete_user_FAIL(self):
        """Expected failure as mods cant delete users onyl change them"""
        pass

    def test_regular_user_change_delete_FAIL(self):
        pass
