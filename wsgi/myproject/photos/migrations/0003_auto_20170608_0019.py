# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_album_albumphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumphoto',
            name='image',
            field=models.ForeignKey(to='photos.BasicPhoto', related_name='images'),
        ),
    ]
