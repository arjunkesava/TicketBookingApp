from django.conf.urls import url

from . import views

app_name = 'Book'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #url(r'^(?P<string3>\w+/[\w\-]+/\d{4}-[01]\d-[0-3]\d/(show1|show2))/$', views.triple_element, name='triple_element'),
    #url(r'^(?P<string1>\w+)/$', views.single_element, name='single_element'),
    #url(r'^(?P<string2>data/double/)/$', views.double_element, name='double_element'),

    # w+ is for theater+names
    # w_ is for movie_names
    # Theater / Movie / Date / Time
    # T/M   T/D     T/ti     M/D     M/Ti       D/Ti
    # T/M/D     T/M/Ti  T/D/Ti
    # T/M/D/Ti

    url(r'^(?P<string1>[\w\_]+/|[\w\+]+/|\d{4}-[01]\d-[0-3]\d/|(morning_show|afternoon_show|first_show|second_show))$', views.single_element),

    url(r'^(?P<string2>[\w\+]+/[\w\_]+/|[\w\+]+/\d{4}-[01]\d-[0-3]\d/)$', views.double_element),
    url(r'^(?P<string2>[\w\+]+/(morning_show|afternoon_show|first_show|second_show)/|[\w\_]+/\d{4}-[01]\d-[0-3]\d/)$', views.double_element),
    url(r'^(?P<string2>[\w\_]+/(morning_show|afternoon_show|first_show|second_show)/)$', views.double_element),
    url(r'^(?P<string2>\d{4}-[01]\d-[0-3]\d/(morning_show|afternoon_show|first_show|second_show)/)$', views.double_element),

    url(r'^(?P<string3>[\w\+]+/[\w\_]+/\d{4}-[01]\d-[0-3]\d/)$', views.triple_element),
    url(r'^(?P<string4>[\w\+]+/[\w\_]+/\d{4}-[01]\d-[0-3]\d/(morning_show|afternoon_show|first_show|second_show))$', views.quad_element),

    '''
    url(r'^movie/(?P<url_movie_id>[0-9]+)/$', views.movie, name='movie'),
    url(r'^movie/any-movie', views.index, name='index'),

    url(r'^theater/any-theater', views.index, name='index'),
    url(r'^theater/(?P<theaterid>[0-9]+)/$', views.theater, name='theater'),

    url(r'^showdate/any-date', views.index, name='index'),
    url(r'^showdate/(?P<url_showdate>[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])+)/$', views.date, name='date'),

    [\w\+]+/[\w\-]+/|[\w\+]+/\d{4}-[01]\d-[0-3]\d/|[\w\+]/(morning_show|afternoon_show|first_show|second_show)
    '''
    ]


# book/ theater/2001/  movie/1001/   showdate/2016-12-11
