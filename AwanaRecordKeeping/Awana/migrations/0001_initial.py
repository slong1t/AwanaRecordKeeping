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
                ('current_book', models.CharField(max_length=2, choices=[('0', 'Flight 3:16'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')])),
                ('name', models.CharField(max_length=30)),
                ('dues', models.DecimalField(default=0.0, max_digits=6, decimal_places=2)),
                ('current_chapter', models.IntegerField(null=True, default=0)),
                ('current_section', models.IntegerField(null=True, default=0)),
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
                ('version', models.IntegerField(default=0)),
                ('present', models.BooleanField(default=False)),
                ('kid', models.ForeignKey(null=True, to='Awana.Clubber')),
            ],
        ),
        migrations.CreateModel(
            name='HandBookPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('book', models.CharField(max_length=2, blank=True, null=True, choices=[('0', 'Flight 3:16'), ('1', 'Sparks HangGlider'), ('2', 'Sparks WingRunner'), ('3', 'Sparks SkyStormer'), ('4', 'T&T Start Zone'), ('5', 'T&T Grace In Action'), ('6', 'T&T Adventure Book1'), ('7', 'T&T Adventure Book2'), ('8', 'T&T Challenge Book1'), ('9', 'T&T Challenge Book2'), ('10', 'Cubbie Appleseed'), ('11', 'Cubbie HoneyComb'), ('12', 'Puggle')])),
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
