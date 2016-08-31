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
from users.forms import RegisterForm

router = routers.DefaultRouter()
router.register(r'users', users.views.UserViewSet)

# Use this to override registration/login; i.e. DRY for login template
login_template = {'template_name': 'rest_framework/login.html'}

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="base.html")),

    # Next two URLS are for public user registration
    # For displaying messages/data in /success, use a CBV constructed
    # from both SuccessMessageMixin + CreateView
    url(r"^success/$", TemplateView.as_view(template_name="registration/success.html")),
    url(r'^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=RegisterForm,
            success_url='/success/'
    ), name='create_normal_user'),

    # change password, etc
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/',  auth_views.login, login_template, name="login"),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls, namespace="api")),

    url(r'^api-token-auth/', token_views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
