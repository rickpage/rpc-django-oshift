from django.db.models.signals import pre_migrate,pre_init
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver

"""
If this doesn't run, can do manually in the shell:

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
content_type = ContentType.objects.get_for_model(User)
Permission.objects.get_or_create(codename='view_user', name='View user', content_type=content_type)

for more details http://stackoverflow.com/questions/7724265/how-to-add-custom-permission-to-the-user-model-in-django
"""

# custom user related permissions
@receiver(pre_init, sender=auth_models)
def add_user_permissions(sender, **kwargs):
    # TODO: use get user model () instead of hardcoded. Cannot pass string to this function
    content_type = ContentType.objects.get_for_model(User)
    Permission.objects.get_or_create(codename='view_user', name='View user', content_type=content_type)
