# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0011_auto_20170108_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatingtable',
            name='seatclassname',
            field=models.CharField(max_length=100),
        ),
    ]
