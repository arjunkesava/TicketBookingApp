# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0007_remove_theatershowtimings_theaterbase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieactivedays',
            old_name='showenddate',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='movieactivedays',
            name='showfromdate',
        ),
    ]
