# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0005_activeshowtimings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activeshowtimings',
            name='id',
        ),
        migrations.AddField(
            model_name='activeshowtimings',
            name='activeshowid',
            field=models.CharField(max_length=100, primary_key=True, default=5000, serialize=False),
            preserve_default=False,
        ),
    ]
