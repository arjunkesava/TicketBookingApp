# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookedRecords',
            fields=[
                ('booktime', models.DateTimeField()),
                ('showtime', models.DateTimeField()),
                ('numberoftickets', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('seatslist', models.TextField()),
                ('bookid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MovieActiveDays',
            fields=[
                ('showdate', models.DateField()),
                ('activedayid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MovieDetails',
            fields=[
                ('moviename', models.CharField(max_length=200)),
                ('movierating', models.IntegerField()),
                ('movieposter', models.ImageField(upload_to='media/')),
                ('movieid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SeatingTable',
            fields=[
                ('seatlayouttext', models.TextField(max_length=5000)),
                ('seatingid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TheaterBase',
            fields=[
                ('location', models.CharField(max_length=200)),
                ('theatername', models.CharField(max_length=500)),
                ('totalseats', models.IntegerField()),
                ('theaterid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TheaterShowTimings',
            fields=[
                ('showname', models.CharField(max_length=100)),
                ('showtime', models.TimeField()),
                ('theatershowtimingsid', models.IntegerField(primary_key=True, serialize=False)),
                ('theaterbase', models.ForeignKey(to='Book.TheaterBase')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('mailaddress', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=100)),
                ('userid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='seatingtable',
            name='theaterbase',
            field=models.ForeignKey(to='Book.TheaterBase'),
        ),
        migrations.AddField(
            model_name='movieactivedays',
            name='moviedetails',
            field=models.ForeignKey(to='Book.MovieDetails'),
        ),
        migrations.AddField(
            model_name='movieactivedays',
            name='theaterbase',
            field=models.ForeignKey(to='Book.TheaterBase'),
        ),
        migrations.AddField(
            model_name='bookedrecords',
            name='moviedetails',
            field=models.ForeignKey(to='Book.MovieDetails'),
        ),
        migrations.AddField(
            model_name='bookedrecords',
            name='seatingtable',
            field=models.ForeignKey(to='Book.SeatingTable'),
        ),
        migrations.AddField(
            model_name='bookedrecords',
            name='theaterbase',
            field=models.ForeignKey(to='Book.TheaterBase'),
        ),
        migrations.AddField(
            model_name='bookedrecords',
            name='userdetails',
            field=models.ForeignKey(to='Book.UserDetails'),
        ),
    ]
