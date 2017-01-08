from django.contrib import admin
from .models import UserDetails, MovieDetails, TheaterBase, SeatingTable, BookedRecords, TheaterShowTimings, MovieActiveDays, ActiveShowTimings

class MovieActiveDaysAdmin(admin.ModelAdmin):
    fields = ['moviedetails','theaterbase','date']
    list_display = ('date', 'moviedetails','theaterbase')
    list_filter =['date', 'moviedetails', 'theaterbase']

class TheaterShowTimingsAdmin(admin.ModelAdmin):
    list_display = ('showname','showtime')
    list_filter = ['showtime','showname']


admin.site.register(UserDetails)
#admin.site.register(MovieDetails)
#admin.site.register(TheaterBase)
admin.site.register(SeatingTable)
admin.site.register(BookedRecords)
admin.site.register(TheaterShowTimings, TheaterShowTimingsAdmin)
admin.site.register(MovieActiveDays, MovieActiveDaysAdmin)
admin.site.register(ActiveShowTimings)
