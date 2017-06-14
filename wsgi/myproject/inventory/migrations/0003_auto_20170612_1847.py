# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20170612_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquantity',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
