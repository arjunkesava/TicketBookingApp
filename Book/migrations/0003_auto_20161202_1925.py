# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0002_auto_20161202_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieactivedays',
            old_name='showdate',
            new_name='showenddate',
        ),
        migrations.AddField(
            model_name='movieactivedays',
            name='showfromdate',
            field=models.DateField(default=datetime.date(2016, 12, 2)),
            preserve_default=False,
        ),
    ]
