# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0012_auto_20170108_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatingtable',
            name='seatclassamount',
            field=models.IntegerField(default=90),
            preserve_default=False,
        ),
    ]
