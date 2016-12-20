from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import UserDetails, MovieDetails, TheaterBase, SeatingTable, BookedRecords, TheaterShowTimings, MovieActiveDays, ActiveShowTimings
import time
import json
from datetime import datetime, timedelta
from django.core import serializers
import re

# The Notes link is https://shrib.com/9gzBoNbh8HIrnqC
def index(request):
    #### Active Dates Data
    current_date = time.strftime("%Y-%m-%d")
    end_date = datetime.now() + timedelta(days=7)
    end_date = end_date.strftime("%Y-%m-%d")
    active_dates_content = MovieActiveDays.objects.filter(date=current_date).distinct()

    today_movies_list = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()
    today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=current_date).distinct()

    ## Array to print current + 6 days
    today_dates_list = {}
    for x in range(0, 6):
        showdate = datetime.now() + timedelta(days=x)
        today_dates_list["/book/" + showdate.strftime('%Y-%m-%d')] = showdate

    #TODO: store the show names into {}
    show_name_list = TheaterShowTimings.objects.all().distinct()
    today_show_name_list = {}
    for item in show_name_list:
        temp = item.showname.split('_')
        today_show_name_list[item.showname] = temp[0].title()+' '+temp[1].title()



    #request.session['session_movies_list'] = serializers.serialize("json",today_movies_list_names)
    #request.session['session_movies_list'] = 'dada'
    request.session['selected_moviename'] = 'Select Movie Name'
    request.session['selected_theatername'] = 'Select Theater Name'
    request.session['selected_showdate'] = 'Select Date'
    request.session['selected_showname'] = 'Select Show Time'
    request.session['selected_moviename_id'] = None
    request.session['selected_theatername_id'] = None
    request.session['selected_showdate_id'] = None
    request.session['selected_showname_id'] = None
    request.session['current_date'] = current_date
    request.session['end_date'] = end_date

    return render(request, 'Book/base_active_area_content.html', {'active_dates_content': active_dates_content,
                                                                  'today_movies_list': today_movies_list,
                                                                  'today_movies_list_names': today_movies_list,     # the same id for both names
                                                                  'weeklist': today_dates_list,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'today_show_name_list': today_show_name_list,
                                                                  'selected_moviename': 'Select Movie Name',
                                                                  'selected_theatername': 'Select Theater Name',
                                                                  'selected_showdate': 'Select Date',
                                                                  'selected_showname': 'Select Show Time',
                                                                  })


def single_element(request, string1):               # retrieves only single element
    url_list = string1.split('/')
    url_list = url_list[0]

    current_date = request.session.get('current_date')
    today_dates_list = today_show_name_list = {}

    if bool(re.compile(r'([\w\_]+)$').match(url_list)):  # the url is a movie
        match = 'movie'
        today_movies_list = MovieDetails.objects.filter(movieactivedays__moviedetails=url_list, movieactivedays__date=current_date).distinct()
        today_movies_list_names = MovieDetails.objects.all()

        for item in today_movies_list_names:
            item.movieid = "/book/"+item.movieid

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/"+item.theaterid+"/"+url_list

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__moviedetails=url_list, movieactivedays__showfromdate__lte=showdate, movieactivedays__showenddate__gte=showdate).values_list('movieid', 'moviename').distinct().exists()):
                today_dates_list["/book/"+url_list+"/"+showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.all().distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        temp = MovieDetails.objects.filter(movieid=url_list).values('moviename').distinct()
        try:
            request.session['selected_moviename'] = temp[0]['moviename']
            request.session['selected_theatername'] = 'Select Theater Name'
            request.session['selected_showdate'] = 'Select Show Date'
            request.session['selected_showtime'] = 'Select Show Time'
        except Exception:
            request.session['selected_moviename'] = 'Select Movie Name'

    elif bool(re.compile(r'([\w\+]+)$').match(url_list)):     # the url is a theater
        match = 'theater'
        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list, movieactivedays__date=current_date).distinct()
        today_movies_list_names = today_movies_list

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__theaterbase=url_list, movieactivedays__date=showdate).values('movieid').distinct().exists()):
                today_dates_list["/book/" + url_list + "/" + showdate.strftime('%Y-%m-%d')] = showdate
        today_theater_list_names = TheaterBase.objects.all()

        show_name_list = TheaterShowTimings.objects.all().distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        temp = TheaterBase.objects.filter(theaterid=url_list).values('theatername').distinct()
        try:
            request.session['selected_moviename'] = 'Select Movie Name'
            request.session['selected_theatername'] = temp[0]['theatername']
            request.session['selected_showdate'] = 'Select Show Date'
            request.session['selected_showtime'] = 'Select Show Time'
        except Exception:
            request.session['selected_theatername'] = 'Select Theater Name'

    if bool(re.compile(r'(\d{4}-[01]\d-[0-3]\d)$').match(url_list)):     # the url is a showdate
        match = 'date'
        today_movies_list = MovieDetails.objects.filter(movieactivedays__date=url_list).distinct()

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__date=url_list).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=url_list).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list

        today_dates_list = {}
        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            today_dates_list["/book/" + showdate.strftime('%Y-%m-%d')] = showdate

        #show_name_list = TheaterShowTimings.objects.raw('SELECT distinct * FROM Book_TheaterShowTimings where theatershowtimingsid IN (select TheaterShowTimings_id from Book_ActiveShowTimings where MovieActiveDays_id IN (select activedayid from Book_MovieActiveDays where date = %s)) order by showtime ASC', [url_list])
        show_name_list = TheaterShowTimings.objects.filter(MovieActiveDays__date=url_list).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        request.session['selected_theatername'] = 'Select Theater Name'
        request.session['selected_moviename'] = 'Select Movie Name'
        request.session['selected_showdate'] = url_list
        request.session['selected_showtime'] = 'Select Show Time'

    if bool(re.compile(r'(morning_show|afternoon_show|first_show|second_show)$').match(url_list)):  # the url is a showtime
        match = 'showtime'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()
        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=current_date).distinct()

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list

        today_dates_list = {}
        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            today_dates_list["/book/" + showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.all().distinct()
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        request.session['selected_theatername'] = 'Select Theater Name'
        request.session['selected_moviename'] = 'Select Movie Name'
        request.session['selected_showdate'] = 'Select Show Date'
        request.session['selected_showtime'] = url_list

    if today_movies_list.count() == 1:
        template_name = 'Book/base_one_movie_content.html'
    else:
        template_name = 'Book/base_active_area_content.html'

    return render(request, template_name, {'today_movies_list': today_movies_list,
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'weeklist': today_dates_list,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'today_show_name_list': today_show_name_list,
                                                                  'selected_moviename': request.session.get(
                                                                      'selected_moviename'),
                                                                  'selected_theatername': request.session.get(
                                                                      'selected_theatername'),
                                                                  'selected_showdate': request.session.get(
                                                                      'selected_showdate'),
                                                                  'selected_showname': request.session.get(
                                                                      'selected_showname'),
                                                                  'url_list': url_list,
                                                                  'match': match,
                                                                  })


def double_element(request, string2):
    #string2 = url_patterns_parameter(string2)
    #html = "The element I retrived is Double %s " % (string2)
    #return HttpResponse(html)
    url_list = string2.split('/')
    current_date = request.session.get('current_date')

    match = ''
    today_dates_list = today_movies_list = today_movies_list_names = today_theater_list_names = {}
    if bool(re.compile(r'([\w\+]+/[\w\_]+)$').match(url_list[0]+'/'+url_list[1])):     # theater and movie url
        match = 'theater/movie/'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0], movieactivedays__moviedetails=url_list[1], movieactivedays__date=current_date).distinct()

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0], movieactivedays__date=current_date).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/"+url_list[0]+"/"+item.movieid

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list[1]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/"+item.theaterid+"/"+url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__moviedetails=url_list[1], movieactivedays__theaterbase=url_list[0],movieactivedays__date=showdate).values_list('movieid', 'moviename').distinct().exists()):
                today_dates_list["/book/"+url_list[0]+"/"+url_list[1]+"/"+showdate.strftime('%Y-%m-%d')] = showdate

        temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
        request.session['selected_theatername'] = temp[0]['theatername']
        temp = MovieDetails.objects.filter(movieid=url_list[1]).values('moviename').distinct()
        request.session['selected_moviename'] = temp[0]['moviename']

    elif bool(re.compile(r'([\w\+]+/\d{4}-[01]\d-[0-3]\d)$').match(url_list[0]+'/'+url_list[1])):     # theater and date url
        match = 'theater/date/'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                        movieactivedays__date=url_list[1]).distinct()

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[1]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=url_list[1]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                movieactivedays__date=url_list[1]).values_list('movieid', 'moviename').distinct().exists()):
                today_dates_list[
                    "/book/" + url_list[0] + "/" + showdate.strftime('%Y-%m-%d')] = showdate

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[1]

    if today_movies_list.count() == 1:
        template_name = 'Book/base_one_movie_content.html'
    else:
        template_name = 'Book/base_active_area_content.html'

    return render(request, template_name, {'today_movies_list': today_movies_list,
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'weeklist': today_dates_list,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'selected_moviename': request.session.get(
                                                                      'selected_moviename'),
                                                                  'selected_theatername': request.session.get(
                                                                      'selected_theatername'),
                                                                  'selected_showdate': request.session.get(
                                                                      'selected_showdate'),
                                                                  'selected_showname': request.session.get(
                                                                      'selected_showtime'),
                                                                  'url_list': url_list,
                                                                  'match': match,
                                                                  })


def triple_element(request, string3):
    html = "The element I retrived is triple %s " % (string3)
    return HttpResponse(html)
def quad_element(request, string4):
    html = "The element I retrived is quad %s " % (string4)
    return HttpResponse(html)

'''
def url_patterns_parameter(string2):
    url_list = string2.split('/')

    redirect = []
    for x in range(0, 4):
        redirect.insert(x, 0)
    for item in url_list:
        if item != '':
            if bool(re.compile(r'(\d{4}-[01]\d-[0-3]\d)$').match(item)):     # the url is a date
                redirect[2] = item
            elif bool(re.compile(r'(\d{4}-[01]\d-[0-3]\d)$').match(item)):  # the url is a show name
                redirect[3] = item
            elif bool(re.compile(r'([\w\_]+)$').match(item)):     # the url is a movie
                redirect[1] = item
            elif bool(re.compile(r'([\w\+]+)$').match(item)):  # the url is a theater
                redirect[0] = item

    return redirect
'''