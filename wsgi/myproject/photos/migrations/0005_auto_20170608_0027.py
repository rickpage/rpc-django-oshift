# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20170608_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumphoto',
            name='image',
            field=models.ImageField(default='album_photo/no-img.jpg', upload_to='album_photo'),
        ),
    ]
