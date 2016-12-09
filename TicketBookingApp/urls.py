from django.conf import settings

"""
Definition of urls for TicketBookingApp.
"""

from django.conf.urls import include, url
from TicketBookingApp.views import index

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', TicketBookingApp.views.home, name='home'),
    # url(r'^TicketBookingApp/', include('TicketBookingApp.TicketBookingApp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index, name='index'),
    url(r'^book/', include('Book.urls', namespace="Book")),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]
