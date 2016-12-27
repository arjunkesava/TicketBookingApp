from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class UserDetails(models.Model):
    mailaddress = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    userid = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.userid

@python_2_unicode_compatible
class MovieDetails(models.Model):
    moviename = models.CharField(max_length=200)
    movierating = models.IntegerField()
    movieposter = models.ImageField(upload_to="media/")  # need to insert image here
    movieid = models.CharField(primary_key=True, max_length=100)
    #linkmovieactivedays = models.ManyToManyField('ActiveShowTimings', through='MovieActiveDays')
    #linkmovieshowtimings = models.ManyToManyField('MovieActiveDays', through='ActiveShowTimings')
    def __str__(self):
        return self.movieid

@python_2_unicode_compatible
class TheaterBase(models.Model):
    location = models.CharField(max_length=200)
    theatername = models.CharField(max_length=500)
    totalseats = models.IntegerField()
    theaterid = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.theaterid

@python_2_unicode_compatible
class SeatingTable(models.Model):
    seatlayouttext = models.TextField(max_length=5000)
    theaterbase = models.ForeignKey(TheaterBase, on_delete=models.CASCADE)
    seatingid = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.seatingid

@python_2_unicode_compatible
class BookedRecords(models.Model):
    booktime = models.DateTimeField()
    showtime = models.DateTimeField()
    numberoftickets = models.IntegerField()
    amount = models.IntegerField()
    seatslist = models.TextField()
    userdetails = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    moviedetails = models.ForeignKey(MovieDetails, on_delete=models.CASCADE)
    seatingtable = models.ForeignKey(SeatingTable, on_delete=models.CASCADE)
    theaterbase = models.ForeignKey(TheaterBase, on_delete=models.CASCADE)
    bookid = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.bookid

@python_2_unicode_compatible
class TheaterShowTimings(models.Model):
    showname = models.CharField(max_length=100)
    showtime = models.TimeField()  # stores only time
    theatershowtimingsid = models.CharField(primary_key=True, max_length=100)
    linkmovieactivedays = models.ManyToManyField('MovieActiveDays', through='ActiveShowTimings')
    def __str__(self):
        return self.theatershowtimingsid

@python_2_unicode_compatible
class MovieActiveDays(models.Model):
    date = models.DateField()  # stores single only date
    moviedetails = models.ForeignKey(MovieDetails, on_delete=models.CASCADE)
    theaterbase = models.ForeignKey(TheaterBase, on_delete=models.CASCADE)
    activedayid = models.CharField(primary_key=True, max_length=100)
    linkshowtimings = models.ManyToManyField('TheaterShowTimings', through='ActiveShowTimings')
    def __str__(self):
        return self.activedayid

@python_2_unicode_compatible
class ActiveShowTimings(models.Model):
    TheaterShowTimings = models.ForeignKey(TheaterShowTimings, on_delete=models.CASCADE)
    MovieActiveDays = models.ForeignKey(MovieActiveDays, on_delete=models.CASCADE)
    activeshowid = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.activeshowid