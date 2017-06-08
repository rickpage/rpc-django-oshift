# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('notes', models.CharField(max_length=1024)),
                ('creator', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlbumPhoto',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('album', models.ForeignKey(related_name='+', to='photos.Album')),
                ('creator', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(related_name='+', to='photos.BasicPhoto')),
            ],
        ),
    ]
