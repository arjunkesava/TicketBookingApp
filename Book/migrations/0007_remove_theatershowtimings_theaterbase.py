# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0006_auto_20161212_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theatershowtimings',
            name='theaterbase',
        ),
    ]
