# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Awana', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubber',
            name='current_chapter',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='clubber',
            name='current_section',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='clubber',
            name='current_book',
            field=models.CharField(max_length=2, choices=[('0', 'Sparks StartZone'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')]),
        ),
        migrations.AlterField(
            model_name='handbookpoint',
            name='book',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('0', 'Sparks StartZone'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')]),
        ),
    ]
