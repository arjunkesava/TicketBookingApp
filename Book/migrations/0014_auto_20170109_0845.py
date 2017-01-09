# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0013_seatingtable_seatclassamount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='password',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='cellnumber',
            field=models.CharField(default='dfsfd', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userdetails',
            name='username',
            field=models.CharField(default='arjun', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookedrecords',
            name='amount',
            field=models.FloatField(),
        ),
    ]
