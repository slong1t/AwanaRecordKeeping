# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Awana', '0002_auto_20171009_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubpoints',
            name='present',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubpoints',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]
