# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_auto_20170608_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumphoto',
            name='album',
            field=models.ForeignKey(to='photos.Album', related_name='images'),
        ),
        migrations.AlterField(
            model_name='albumphoto',
            name='image',
            field=models.ForeignKey(to='photos.BasicPhoto', related_name='+'),
        ),
    ]
