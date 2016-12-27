# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0009_theatershowtimings_movieactivedays'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theatershowtimings',
            old_name='MovieActiveDays',
            new_name='movieactivedays',
        ),
    ]
