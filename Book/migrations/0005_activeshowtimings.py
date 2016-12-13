# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0004_auto_20161210_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveShowTimings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('MovieActiveDays', models.ForeignKey(to='Book.MovieActiveDays')),
                ('TheaterShowTimings', models.ForeignKey(to='Book.TheaterShowTimings')),
            ],
        ),
    ]
