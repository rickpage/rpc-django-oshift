from django.core.urlresolvers import reverse
# TODO: Reverse will change to django.urls >= 1.10
from rest_framework import status
from rest_framework.test import APITestCase
#from myproject.apps.core.models import Account
from django.contrib.auth.models import User

# class AccountTests(APITestCase):
#     def test_create_account(self):
#         """
#         # TODO Move to Users
#         Ensure we can create a new account object.
#         """
#         url = reverse('api:user-list')
#         data = {'username': 'someusername','password':'somepassword'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().name, 'username')
