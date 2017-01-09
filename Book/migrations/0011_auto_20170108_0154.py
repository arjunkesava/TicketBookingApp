# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0010_auto_20161220_0305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theatershowtimings',
            old_name='movieactivedays',
            new_name='linkmovieactivedays',
        ),
        migrations.AddField(
            model_name='movieactivedays',
            name='linkshowtimings',
            field=models.ManyToManyField(to='Book.TheaterShowTimings', through='Book.ActiveShowTimings'),
        ),
        migrations.AddField(
            model_name='seatingtable',
            name='seatclassname',
            field=models.TextField(max_length=100, default='business class'),
            preserve_default=False,
        ),
    ]
