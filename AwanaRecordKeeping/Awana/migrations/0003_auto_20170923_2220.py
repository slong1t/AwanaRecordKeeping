# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Awana', '0002_auto_20170901_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubpoints',
            name='sections_passed',
        ),
        migrations.AddField(
            model_name='clubpoints',
            name='version',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clubber',
            name='current_book',
            field=models.CharField(max_length=2, choices=[('0', 'Flight 3:16'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')]),
        ),
        migrations.AlterField(
            model_name='handbookpoint',
            name='book',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('0', 'Flight 3:16'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')]),
        ),
    ]
