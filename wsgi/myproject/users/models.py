from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#
# Signals
#

# Add Token to user model
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#
# Serializers
#

from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name','first_name', 'email', 'groups', 'password')

        # thanks to http://stackoverflow.com/questions/27468552/changing-serializer-fields-on-the-fly/#answer-27471503
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

class GroupSerializer(serializers.ModelSerializer):
    group_id = serializers.ReadOnlyField(source='id')
    class Meta:
        model = Group
        fields = ('name', 'group_id')
