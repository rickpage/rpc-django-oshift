"""
RPC Django on Openshift
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views

from rest_framework.authtoken import views as token_views
from rest_framework import routers
import users.views
from django.views.generic import TemplateView
# For default registration functionality
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

router = routers.DefaultRouter()
router.register(r'users', users.views.UserViewSet)

login_template = {'template_name': 'rest_framework/login.html'}
#password_change_template = {'template_name': '/password_change.html'}

url('^accounts/password_change/',auth_views.password_change, )
urlpatterns = [
    url('^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/'
    ), name='create_normal_user'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/',  auth_views.login, login_template, name="login"),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls, namespace="api")),

    url(r'^api-token-auth/', token_views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
