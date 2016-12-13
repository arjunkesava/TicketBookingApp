from django.contrib import admin
from .models import UserDetails, MovieDetails, TheaterBase, SeatingTable, BookedRecords, TheaterShowTimings, MovieActiveDays, ActiveShowTimings

admin.site.register(UserDetails)
admin.site.register(MovieDetails)
admin.site.register(TheaterBase)
admin.site.register(SeatingTable)
admin.site.register(BookedRecords)
admin.site.register(TheaterShowTimings)
admin.site.register(MovieActiveDays)
admin.site.register(ActiveShowTimings)
