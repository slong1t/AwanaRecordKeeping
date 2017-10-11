# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Awana', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubpoints',
            name='present',
        ),
        migrations.RemoveField(
            model_name='clubpoints',
            name='version',
        ),
    ]
