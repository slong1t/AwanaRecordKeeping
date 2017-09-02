# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clubber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('club', models.CharField(max_length=1, choices=[('0', 'Puggle'), ('1', 'Cubbie'), ('2', 'Spark'), ('3', 'TnT Girls'), ('4', 'TnT Boys')])),
                ('current_book', models.CharField(max_length=2, choices=[('0', 'Sparks StartZone'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('5', 'T&T Adventure Book1'), ('6', 'T&T Adventure Book2'), ('7', 'T&T Challenge Book1'), ('8', 'T&T Challenge Book2'), ('9', 'Cubbie Appleseed'), ('10', 'Cubbie HoneyComb'), ('11', 'Puggle')])),
                ('name', models.CharField(max_length=30)),
                ('dues', models.DecimalField(default=0.0, max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='ClubPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('bible', models.BooleanField(default=False)),
                ('uniform', models.BooleanField(default=False)),
                ('book', models.BooleanField(default=False)),
                ('visitor', models.BooleanField(default=False)),
                ('sections_passed', models.IntegerField(default=0)),
                ('kid', models.ForeignKey(null=True, to='Awana.Clubber')),
            ],
        ),
        migrations.CreateModel(
            name='HandBookPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('book', models.CharField(max_length=2, blank=True, null=True, choices=[('0', 'Sparks StartZone'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('5', 'T&T Adventure Book1'), ('6', 'T&T Adventure Book2'), ('7', 'T&T Challenge Book1'), ('8', 'T&T Challenge Book2'), ('9', 'Cubbie Appleseed'), ('10', 'Cubbie HoneyComb'), ('11', 'Puggle')])),
                ('chapter', models.IntegerField(null=True)),
                ('section', models.IntegerField(null=True)),
                ('date', models.DateField(null=True)),
                ('clubber', models.ForeignKey(to='Awana.Clubber')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingNight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('attendees', models.ManyToManyField(to='Awana.Clubber')),
            ],
        ),
        migrations.AddField(
            model_name='clubpoints',
            name='night',
            field=models.ForeignKey(null=True, to='Awana.MeetingNight'),
        ),
    ]
