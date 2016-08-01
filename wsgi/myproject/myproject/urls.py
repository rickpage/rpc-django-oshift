"""
RPC Django on Openshift
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views as token_views
from rest_framework import routers
import users.views 

router = routers.DefaultRouter()
router.register(r'users', users.views.UserViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls, namespace="api")),
    url(r'^api-token-auth/', token_views.obtain_auth_token)
]

# custom log in or out
#from django.contrib.auth import views as rest_auth
#
#template_name = {'template_name': 'users/login.html'}
#
#urlpatterns += [
#    url(r'^access/login/$', rest_auth.login, template_name, name='login'),
#    url(r'^access/logout/$', rest_auth.logout, template_name, name='logout'),
#]

# specific to browseable API, though we could use this too if we like
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]