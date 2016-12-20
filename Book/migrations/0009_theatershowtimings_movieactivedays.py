# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0008_auto_20161219_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='theatershowtimings',
            name='MovieActiveDays',
            field=models.ManyToManyField(through='Book.ActiveShowTimings', to='Book.MovieActiveDays'),
        ),
    ]
