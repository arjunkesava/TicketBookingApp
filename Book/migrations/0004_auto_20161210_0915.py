# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0003_auto_20161202_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedrecords',
            name='bookid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='movieactivedays',
            name='activedayid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='moviedetails',
            name='movieid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='seatingtable',
            name='seatingid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='theaterbase',
            name='theaterid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='theatershowtimings',
            name='theatershowtimingsid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='userid',
            field=models.CharField(primary_key=True, serialize=False, max_length=100),
        ),
    ]
