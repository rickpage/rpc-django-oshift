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
import photos.views
import photos.forms

router = routers.DefaultRouter()
router.register(r'users', users.views.UserViewSet)
router.register(r'groups', users.views.GroupViewSet)
router.register(r'photos', photos.views.BasicPhotoViewSet)
router.register(r'albums', photos.views.AlbumViewSet)
router.register(r'album_photo', photos.views.AlbumPhotoViewSet)

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
    # login here overrides the included one below
    url(r'^accounts/login/',  auth_views.login, login_template, name="login"),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls, namespace="api")),

    url(r'^upload-photo/'
      , TemplateView.as_view(template_name='photos/index.html')
      , name='upload-photo-form'),

    url(r'^upload-photo-post/', photos.views.basic_photo_upload, name='upload-photo'),

    url(r'^api-token-auth/', token_views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
