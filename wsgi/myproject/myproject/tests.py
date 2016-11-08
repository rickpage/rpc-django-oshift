from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User,Group,Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

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


class UserAPIAdminGroupTests(APITestCase):
    """
    Should test that:

    Admins can change users
    Admins can delete users
    regular users with no groups cannot change, or delete users
    TODO: regular users cannot view-users

    Do this by creating fixture data that includes an Admin, super user, and
    a regular user. The super user doesnt need to be tested generally speaking.
    There are system level things an Office Admin role does not need to edit -
    such as the groups and the permissions of those groups, perhaps.

    This assumes the django permissions are set up when the test database is
    set up. The fixture data adds i.e. the Group "Admin" and associates
    change and delete auth.user Permission with the group.

    This makes the users_users data groups correct as well.
    """
    fixtures = ['auth_group_permissions', 'users_users', ]

    def setUp(self):
        self.client = APIClient()
        # We have no control over the ids of the permissions, so
        # we grab them by codename and use them to
        # create group level permissions every time we test.
        # Therefore in production we need to make sure we
        # have correct permissions - a better way to manage this
        # is deisred
        ag = Group.objects.get(name="Admin")
        content_type = ContentType.objects.get_for_model(User)
        p = Permission.objects.get_or_create(codename='view_user'
          , name='View user'
          , content_type=content_type)
        # this also tests the custom view_user for auth user
        codenames = ["change_user","delete_user","view_user"]
        for c in codenames:
            p = Permission.objects.get(codename=c)
            ag.permissions.add(p)
        ag.save()

    def test_regular_user_cant_view_user_api(self):
        """
        Ensure we can't view account object.
        """
        url = reverse('api:user-detail',kwargs={"pk":1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_change_user(self):
        self.assertTrue(self.client.login(username="admin_ttt",password="ttt"))
        # get user
        url = reverse('api:user-detail',kwargs={"pk":1})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # change a detail
        url = reverse('api:user-detail',kwargs={"pk":3})
        data = response.data
        data["last_name"] = "CHANGED"
        data["password"] = "whatever"
        print(data)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK or status.HTTP_201_CREATED or status.HTTP_202_ACCEPTED)

        # confirm the detail by getting user again
        pass

    def test_admin_delete_user(self):
        # get user
        # delete him
        # verify the user is gone
        pass
