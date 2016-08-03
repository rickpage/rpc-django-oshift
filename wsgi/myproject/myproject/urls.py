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
    
    url(r'^$', include(router.urls, namespace="api")),

    url(r'^api-token-auth/', token_views.obtain_auth_token), 
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]