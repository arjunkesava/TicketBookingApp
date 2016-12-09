from django.conf.urls import url

from . import views

app_name = 'Book'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<url_movie_id>[0-9]+)/$', views.movie, name='movie'),
    url(r'^movie/any-movie', views.index, name='index'),

    url(r'^theater/any-theater', views.index, name='index'),
    url(r'^theater/(?P<theaterid>[0-9]+)/$', views.theater, name='theater'),

    url(r'^showdate/any-date', views.index, name='index'),
    url(r'^showdate/(?P<url_showdate>[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])+)/$', views.date, name='date'),
    ]


# book/ theater/2001/  movie/1001/   showdate/2016-12-11
