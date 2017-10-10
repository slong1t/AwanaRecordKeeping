# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Awana', '0003_auto_20170923_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubpoints',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
