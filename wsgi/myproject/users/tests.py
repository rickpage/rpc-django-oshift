from django.test import TestCase
# User model
from  django.contrib.auth import get_user_model
# public reg form
from .forms import RegisterForm
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserUnitTests(TestCase):
    """This tests creation of the user from the form, and NOT the rest API.
    The rest api won't allow deviation from the permissions, but the
    form here does.
    Also ensures the resr API tokens are generated (signal test)"""
    fixtures = ['users_users']
    #,'users_token'] # token is added by post save, dont need one

    def test_fixture_sanity(self):
        '''
        Fixture sanity check. If this fails, the fixture data is bad.
        This happens to tests the post_save on User model...
        '''
        u = get_user_model().objects.get(id=1)
        self.assertFalse(u is None)
        t = Token.objects.get(user_id=u.id)
        self.assertTrue(t is not None and t.user_id == u.id);

    def test_forms_fail(self):
        print("Testing form failure")
        form_data = {'something': 'something'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def _create_user_from_form(self, username, password):
        '''
        Helper for creaing user; fails if form invalid
        '''
        form_data = {'username': username,'password1':password,'password2':password}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        # isthat user here?
        u = get_user_model().objects.get(username=username)
        #u = get_user_model().objects.create_user(username, 'lennon@thebeatles.com', password)
        u.save()
        return u

    def test_forms_create_user_success(self):
        print("Testing form success")
        username = 'testform'
        password = 'testformpass'
        u = self._create_user_from_form(username, password)
        self.assertTrue(u is not None and u.username == username)

    def test_token_for_new_user(self):
        '''
        Test for a new user to get an API token.
        Don't use a fixture to implement this test;
         this tests the signal post_save that adds token
        '''
        username = 'testform'
        password = 'testformpass'
        # Could just create user, but since form would be used, call this
        u = self._create_user_from_form(username, password)
        self.assertTrue(u is not None);
        # can we load the token
        t = Token.objects.get(user_id=u.id)
        self.assertTrue(t is not None and t.user_id == u.id);
        print("Token created on ", t.created)
