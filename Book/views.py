from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import UserDetails, MovieDetails, TheaterBase, SeatingTable, BookedRecords, TheaterShowTimings, MovieActiveDays, ActiveShowTimings
import time
import json
import uuid
from datetime import datetime, timedelta
from django.core import serializers
import re
import pdb

from .forms import SeatingForm, MovieActiveDaysForm, ActiveShowTimingsForm

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
    request.session['current_date'] = current_date
    request.session['end_date'] = end_date


    return render(request, 'Book/base_active_area_content.html', {'active_dates_content': active_dates_content,
                                                                  'today_movies_list': today_movies_list,
                                                                  'today_movies_list_names': today_movies_list,     # the same id for both names
                                                                  'weeklist': today_dates_list,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'today_show_name_list': today_show_name_list,
                                                                  'selected_moviename': request.session.get('selected_moviename'),
                                                                  'selected_theatername': request.session.get('selected_theatername'),
                                                                  'selected_showdate': request.session.get('selected_showdate'),
                                                                  'selected_showname': request.session.get('selected_showname'),
                                                                  })


def single_element(request, string1):               # retrieves only single element
    url_list = string1.split('/')
    url_list = url_list[0]

    current_date = request.session.get('current_date')
    today_dates_list = today_show_name_list = today_theater_list_names = {}
    all_details_of_movie = ''
    count = 0


    if bool(re.compile(r'(morning_show|matinee_show|first_show|second_show)$').match(url_list)):  # the url is a showtime
        match = 'showtime'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__linkshowtimings__showname=url_list).distinct()

        for item in today_movies_list:
            count=count+1


        #today_movies_list_names = list(MovieDetails.objects.raw('select distinct * from Book_MovieDetails where movieid IN (select moviedetails_id from Book_MovieActiveDays where activedayid IN (select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN (select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', [url_list]))
        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__linkshowtimings__showname=url_list).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list


        # today_movies_list = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()
        today_theater_list_names = list(TheaterBase.objects.raw(
            'select distinct * from Book_TheaterBase where theaterid IN'
            '(select theaterbase_id from Book_MovieActiveDays where activedayid IN'
            '(select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN'
            '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', [url_list]
        ))

        #today_theater_list_names = TheaterBase.objects.filter(movieactivedays__showtime=url_list).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list

        today_dates_list = {}
        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            today_dates_list["/book/" + showdate.strftime('%Y-%m-%d') + "/" + url_list] = showdate

        show_name_list = TheaterShowTimings.objects.all().distinct()
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list["/book/" + item.showname] = temp[0].title() + ' ' + temp[1].title()

        showtime = url_list.split('_')
        request.session['selected_showname'] = showtime[0].title() + ' ' + showtime[1].title()

    elif bool(re.compile(r'([\w\_]+)$').match(url_list)):  # the url is a movie
        match = 'movie'
        today_movies_list = MovieDetails.objects.filter(movieactivedays__moviedetails=url_list, movieactivedays__date=current_date).distinct()

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__moviedetails=url_list).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/"+item.movieid

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/"+item.theaterid+"/"+url_list

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__moviedetails=url_list, movieactivedays__date=showdate).distinct().exists()):
                today_dates_list["/book/"+url_list+"/"+showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__moviedetails=url_list).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        temp = MovieDetails.objects.filter(movieid=url_list).values('moviename').distinct()
        try:
            request.session['selected_moviename'] = temp[0]['moviename']
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

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=current_date).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/"+item.theaterid

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__theaterbase=url_list).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        temp = TheaterBase.objects.filter(theaterid=url_list).values('theatername').distinct()
        try:
            request.session['selected_theatername'] = temp[0]['theatername']
        except Exception:
            request.session['selected_theatername'] = 'Select Theater Name'

    elif bool(re.compile(r'(\d{4}-[01]\d-[0-3]\d)$').match(url_list)):     # the url is a showdate
        match = 'date'
        today_movies_list = MovieDetails.objects.filter(movieactivedays__date=url_list).distinct()

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__date=url_list).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=url_list).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list

        today_dates_list = {}
        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            today_dates_list["/book/" + showdate.strftime('%Y-%m-%d')] = showdate

        #show_name_list = TheaterShowTimings.objects.raw(
        # 'SELECT distinct * FROM Book_TheaterShowTimings where theatershowtimingsid IN
        # (select TheaterShowTimings_id from Book_ActiveShowTimings where movieactivedays_id IN
        # (select activedayid from Book_movieactivedays where date = %s)) order by showtime ASC', [url_list])
        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__date=url_list).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        tempdate = url_list.split('-')
        request.session['selected_showdate'] = tempdate[2] + '-' + tempdate[1] + '-' + tempdate[0]

    else:
        today_movies_list = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()

    if count == 1 or today_movies_list.count() == 1:
        template_name = 'Book/base_one_movie_content.html'
        all_details_of_movie = 'The Dynamic Content Will be Displayed here'
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
                                                                  'all_details_of_movie': all_details_of_movie,
                                                                  })

def double_element(request, string2):
    #string2 = url_patterns_parameter(string2)
    #html = "The element I retrived is Double %s " % (string2)
    #return HttpResponse(html)
    url_list = string2.split('/')
    current_date = request.session.get('current_date')
    count = 0

    match = ''
    today_dates_list = today_movies_list = today_movies_list_names = today_theater_list_names = today_show_name_list = {}

    # M/Ti
    if bool(re.compile(r'([\w\_]+/(morning_show|matinee_show|first_show|second_show))$').match(url_list[0] + '/' + url_list[1])): # movie & showtime
        match = 'movie/showtime'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__moviedetails=url_list[0]).distinct()
        for i in today_movies_list:
            count += 1

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__date=current_date).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list[1]

        show_name_list = TheaterShowTimings.objects.all().distinct().order_by('showtime')

        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list["/book/" + url_list[0] + "/" + item.showname] = temp[0].title() + ' ' + temp[1].title()

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieActiveDays.objects.filter(date=showdate, moviedetails=url_list[0], theatershowtimings__showname=url_list[1]).distinct()):
                today_dates_list["/book/" + url_list[0] + "/" + showdate.strftime('%Y-%m-%d') + "/" + url_list[1]] = showdate

        today_theater_list_names = list(TheaterBase.objects.raw('select theaterid,theatername from Book_TheaterBase where theaterid IN '
                                                                '(select theaterbase_id from Book_MovieActiveDays where moviedetails_id = %s and activedayid IN '
                                                                '(select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN '
                                                                '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', (url_list[0], url_list[1])))

        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[0] + "/" + url_list[1]
    # M/D
    elif bool(re.compile(r'([\w\_]+/\d{4}-[01]\d-[0-3]\d)$').match(url_list[0] + '/' + url_list[1])):
        match = 'Movie/Date'

        today_movies_list = MovieDetails.objects.filter(movieid=url_list[0], movieactivedays__date=url_list[1]).distinct()

        for i in today_movies_list:
            count += 1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list[1]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list[0], movieactivedays__date=url_list[1]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[0] + "/" + url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieid=url_list[0],
                                                movieactivedays__date=url_list[1]).distinct().exists()):
                today_dates_list[
                    "/book/" + url_list[0] + "/" + showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__moviedetails=url_list[0],
                                                           movieactivedays__date=url_list[1]).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[1]
    # D/Ti
    elif bool(re.compile(r'(\d{4}-[01]\d-[0-3]\d/(morning_show|matinee_show|first_show|second_show))$').match(url_list[0] + '/' + url_list[1])):
        match = 'date/Showtime'

        #today_movies_list = MovieDetails.objects.filter(movieactivedays__date=url_list[0], movieactivedays__showname=url_list[1]).distinct()
        today_movies_list = list(MovieDetails.objects.raw(
            'select distinct * from Book_MovieDetails where movieid IN '
            '(select moviedetails_id from Book_MovieActiveDays where date = %s and activedayid IN '
            '(select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN '
            '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', (url_list[0], url_list[1])))

        for i in today_movies_list:
            count += 1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + item.movieid + "/" + url_list[0] + "/" + url_list[1]

        today_theater_list_names = list(TheaterBase.objects.raw(
            'select theaterid,theatername from Book_TheaterBase where theaterid IN '
            '(select theaterbase_id from Book_MovieActiveDays where date = %s and activedayid IN '
            '(select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN'
            '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))',(url_list[0],url_list[1])))
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[0] + "/" + url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieActiveDays.objects.filter(date=url_list[0], theatershowtimings__showname=url_list[1]).distinct()):
                today_dates_list["/book/" + showdate.strftime('%Y-%m-%d') + "/" + url_list[1]] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__date=url_list[0],showname=url_list[1]).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()
    # T/Ti
    elif bool(re.compile(r'([\w\+]+/(morning_show|matinee_show|first_show|second_show))$').match(url_list[0] + '/' + url_list[1])):  # theater and showname url
        match = 'theater/showname/'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                        movieactivedays__linkshowtimings__showname=url_list[1]).distinct()
        '''
        today_movies_list = list(MovieDetails.objects.raw(
            'select distinct * from Book_MovieDetails where movieid IN'
            '(select moviedetails_id from Book_MovieActiveDays where activedayid IN'
            '(select MovieActiveDays_id from Book_ActiveShowTimings where theaterbase_id = %s and TheaterShowTimings_id IN'
            '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', (url_list[0], url_list[1])
        ))
        '''

        for i in today_movies_list:
            count+=1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[1]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__date=request.session['current_date']).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(TheaterBase.objects.filter(theaterid=url_list[0],
                                               movieactivedays__date=showdate).exists()):
                today_dates_list["/book/" + url_list[0] + "/" + showdate.strftime('%Y-%m-%d') + "/" + url_list[1]] = showdate
            '''
            if bool(list(TheaterBase.objects.raw(
                                'select theaterid from Book_TheaterBase where theaterid = %s and theaterid IN '
                                '(select theaterbase_id from Book_MovieActiveDays where activedayid IN '
                                '(select MovieActiveDays_id from Book_ActiveShowTimings where TheaterShowTimings_id IN '
                                '(select theatershowtimingsid from Book_TheaterShowTimings where showname = %s)))', (url_list[0], url_list[1])))):
                        '''

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__theaterbase=url_list[0]).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[1]
    # T/M/
    elif bool(re.compile(r'([\w\+]+/[\w\_]+)$').match(url_list[0]+'/'+url_list[1])):     # theater and movie url
        match = 'theater/movie/'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0], movieactivedays__moviedetails=url_list[1], movieactivedays__date=current_date).distinct()

        for i in today_movies_list:
            count+=1

        today_movies_list_names = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0], movieactivedays__date=current_date).distinct()
        for item in today_movies_list_names:
            item.movieid = "/book/"+url_list[0]+"/"+item.movieid

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list[1]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/"+item.theaterid+"/"+url_list[1]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__moviedetails=url_list[1], movieactivedays__theaterbase=url_list[0], movieactivedays__date=showdate).values_list('movieid', 'moviename').distinct().exists()):
                today_dates_list["/book/"+url_list[0]+"/"+url_list[1]+"/"+showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__moviedetails=url_list[1], movieactivedays__theaterbase=url_list[0]).distinct().order_by('-showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list["/book/"+url_list[0]+"/"+url_list[1]+"/"+item.showname] = temp[0].title() + ' ' + temp[1].title()

        temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
        request.session['selected_theatername'] = temp[0]['theatername']
        temp = MovieDetails.objects.filter(movieid=url_list[1]).distinct()
        for item in temp:
            request.session['selected_moviename'] = item.moviename
    # T/D
    elif bool(re.compile(r'([\w\+]+/\d{4}-[01]\d-[0-3]\d)$').match(url_list[0]+'/'+url_list[1])): # theater and date url
        match = 'theater/date/'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                        movieactivedays__date=url_list[1]).distinct()

        for i in today_movies_list:
            count+=1

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

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                           movieactivedays__date=url_list[1]).distinct().order_by('showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[1]



    if count == 1:
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

def triple_element(request, string3):
    url_list = string3.split('/')
    current_date = request.session.get('current_date')
    count = 0

    match = ''
    today_dates_list = today_movies_list = today_movies_list_names = today_theater_list_names = today_show_name_list = {}

    # T/M/D
    if bool(re.compile(r'([\w\+]+/[\w\_]+/\d{4}-[01]\d-[0-3]\d)$').match(url_list[0]+'/'+url_list[1]+'/'+url_list[2])):
        match = 'theater/movie/date'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                        movieid=url_list[1],
                                                        movieactivedays__date=url_list[2]).distinct()

        for i in today_movies_list:
            count += 1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[2]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list[1],
                                                              movieactivedays__date=url_list[2]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1] + "/" + url_list[2]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieid=url_list[1],
                                                movieactivedays__date=url_list[2]).distinct().exists()):
                today_dates_list[
                    "/book/" + url_list[0] + "/" + url_list[1] + "/" + showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__moviedetails=url_list[1],
                                                           movieactivedays__date=url_list[2]).distinct().order_by(
            'showtime')
        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[2]
    # T/M/Ti
    elif bool(re.compile(r'([\w\+]+/[\w\_]+/(morning_show|matinee_show|first_show|second_show))$').match(url_list[0]+'/'+url_list[1]+'/'+url_list[2])):
        match = 'theater/movie/showtime'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0], movieid=url_list[1],
                                                        movieactivedays__linkshowtimings__showname=url_list[2]).distinct()

        for i in today_movies_list:
            count += 1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[2]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__moviedetails=url_list[1],
                                                              movieactivedays__linkshowtimings__showname=url_list[2]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1] + "/" + url_list[2]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieid=url_list[1],
                                                movieactivedays__theaterbase=url_list[0],
                                                movieactivedays__date=showdate,
                                                movieactivedays__linkshowtimings__showname=url_list[2]).distinct().exists()):
                today_dates_list[
                    "/book/" + url_list[0] + "/" + url_list[1] + "/" + showdate.strftime('%Y-%m-%d')] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                           movieactivedays__moviedetails=url_list[1],
                                                           movieactivedays__linkshowtimings__showname=url_list[2]).distinct().order_by(
            'showtime')

        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[2]
    # T/D/Ti
    elif bool(re.compile(r'([\w\+]+/\d{4}-[01]\d-[0-3]\d/(morning_show|matinee_show|first_show|second_show))').match(url_list[0]+'/'+url_list[1]+'/'+url_list[2])):
        match = 'theater/date/showtime'

        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                        movieactivedays__date=url_list[1],
                                                        movieactivedays__linkshowtimings__showname=url_list[2]).distinct()

        for i in today_movies_list:
            count += 1

        today_movies_list_names = today_movies_list
        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[1] + "/" + url_list[2]

        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                              movieactivedays__date=url_list[1],
                                                              movieactivedays__linkshowtimings__showname=url_list[2]).distinct()
        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1] + "/" + url_list[2]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                movieactivedays__date=showdate,
                                                movieactivedays__linkshowtimings__showname=url_list[2]).distinct().exists()):
                today_dates_list[
                    "/book/" + url_list[0] + "/" + showdate.strftime('%Y-%m-%d') + "/" + url_list[2]] = showdate

        show_name_list = TheaterShowTimings.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                           movieactivedays__date=url_list[1],
                                                           movieactivedays__linkshowtimings__showname=url_list[2]).distinct().order_by(
            'showtime')

        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list[item.showname] = temp[0].title() + ' ' + temp[1].title()

        try:
            temp = TheaterBase.objects.filter(theaterid=url_list[0]).values('theatername').distinct()
            request.session['selected_theatername'] = temp['theatername']
        except Exception:
            request.session['selected_theatername'] = "Select Theater Name"
        request.session['selected_showdate'] = url_list[2]


    if count == 1:
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

def quad_element(request, string4):
    url_list = string4.split('/')
    current_date = request.session.get('current_date')
    count = 0

    match = ''
    today_dates_list = today_movies_list = today_movies_list_names = today_theater_list_names = today_show_name_list = {}

    if bool(re.compile(r'([\w\+]+/[\w\_]+/\d{4}-[01]\d-[0-3]\d/(morning_show|matinee_show|first_show|second_show))').match(url_list[0] + '/' + url_list[1] + '/' + url_list[2] + '/' + url_list[3])):
        match = "theater/movie/date/showtime"

        today_movies_list = MovieDetails.objects.filter(
            movieactivedays__theaterbase=url_list[0],
            movieid=url_list[1],
            movieactivedays__date=url_list[2],
            movieactivedays__linkshowtimings__showname=url_list[3]
        ).distinct()

        for i in today_movies_list:
            count+=1

        today_movies_list_names = MovieDetails.objects.filter(
            movieactivedays__theaterbase=url_list[0],
            movieactivedays__date=url_list[2],
            movieactivedays__linkshowtimings__showname=url_list[3]
        ).distinct()

        for item in today_movies_list_names:
            item.movieid = "/book/" + url_list[0] + "/" + item.movieid + "/" + url_list[2] + "/" + url_list[3]

        today_theater_list_names = TheaterBase.objects.filter(
            movieactivedays__moviedetails=url_list[1],
            movieactivedays__date=url_list[2],
            movieactivedays__linkshowtimings__showname=url_list[3]
        ).distinct()

        for item in today_theater_list_names:
            item.theaterid = "/book/" + item.theaterid + "/" + url_list[1] + "/" + url_list[2] + "/" + url_list[3]

        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__theaterbase=url_list[0],
                                                movieid=url_list[1],
                                                movieactivedays__date=showdate,
                                                movieactivedays__linkshowtimings__showname=url_list[3]).distinct().exists()):
                today_dates_list["/book/" + url_list[0] + "/" + url_list[1] + "/" + showdate.strftime('%Y-%m-%d') + "/" + url_list[3]] = showdate


        show_name_list = TheaterShowTimings.objects.filter(
            movieactivedays__theaterbase=url_list[0],
            movieactivedays__moviedetails=url_list[1],
            movieactivedays__date=url_list[2],
        ).distinct().order_by('-showtime')

        today_show_name_list = {}
        for item in show_name_list:
            temp = item.showname.split('_')
            today_show_name_list["/book/" + url_list[0] + "/" + url_list[1] + "/" + url_list[2] + "/" + item.showname] = temp[0].title() + ' ' + temp[1].title()

        if count == 1:
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


def ownadmin_movieactivedays(request):
    form = {}
    formstatus = "Not Done"
    if request.method == 'POST':
        form = MovieActiveDaysForm(request.POST)
        if form.is_valid():

            new_values = form.save(commit=False)

            from_date_field = form.cleaned_data['from_date_field']
            end_date_field = form.cleaned_data['end_date_field']
            moviedetails = form.cleaned_data['moviedetails']
            theaterbase = form.cleaned_data['theaterbase']

            from_date_field = datetime.strptime(str(from_date_field), "%Y-%m-%d")
            end_date_field = datetime.strptime(str(end_date_field), "%Y-%m-%d")

            for x in range(abs((end_date_field - from_date_field).days)+1):
                showdate = from_date_field + timedelta(days=x)
                new_values.date = showdate.strftime('%Y-%m-%d')
                new_values.moviedetails = moviedetails
                new_values.theaterbase = theaterbase
                new_values.activedayid = uuid.uuid4()
                new_values.save()

            #form.save()
            formstatus = "Done"
        else:
            form = MovieActiveDaysForm()

    return render(request, 'Book/base_ticket_admin_area.html', {'formstatus': formstatus, 'forms': form})

def ownadmin_activeshowtimings(request):
    form = {}
    formstatus = "Not Done Yet"
    morning_show_values = ''
    active_show_timings_list = TheaterShowTimings.objects.all().distinct().order_by('showtime')
    for item in active_show_timings_list:
        tempdate = datetime.strptime(str(item.showtime), "%H:%M:%S")
        item.showtime = tempdate.strftime("%H:%M:%S")
    if request.method == 'POST':
        form = ActiveShowTimingsForm(request.POST)
        if form.is_valid():
            #new_active_values = form.save(commit=False)
            new_active_values = ActiveShowTimings()

            from_date_field = form.cleaned_data['from_date_field']
            end_date_field = form.cleaned_data['end_date_field']
            moviedetails = form.cleaned_data['moviedetails']
            theaterbase = form.cleaned_data['theaterbase']
            morning_show_values = request.POST.getlist('morning_showtime')
            matinee_show_values = request.POST.getlist('matinee_showtime')
            first_show_values = request.POST.getlist('first_showtime')
            second_show_values = request.POST.getlist('second_showtime')

            from_date_field = datetime.strptime(str(from_date_field), "%Y-%m-%d")
            end_date_field = datetime.strptime(str(end_date_field), "%Y-%m-%d")
            for x in range(abs((end_date_field - from_date_field).days) + 1):
                showdate = from_date_field + timedelta(days=x)
                movie_active_id = MovieActiveDays.objects.get(date=showdate, moviedetails=moviedetails, theaterbase=theaterbase)# returns single value

                for itemtime in morning_show_values:
                    theater_show_timings_id = TheaterShowTimings.objects.get(showname='morning_show', showtime=itemtime)
                    new_active_values.MovieActiveDays_id = new_active_values.movieactivedays = movie_active_id.activedayid
                    new_active_values.TheaterShowTimings_id = new_active_values.theatershowtimings = theater_show_timings_id.theatershowtimingsid
                    new_active_values.activeshowid = uuid.uuid4()
                    new_active_values.save()

                for itemtime in matinee_show_values:
                    theater_show_timings_id = TheaterShowTimings.objects.get(showname='matinee_show', showtime=itemtime)
                    new_active_values.MovieActiveDays_id = new_active_values.movieactivedays = movie_active_id.activedayid
                    new_active_values.TheaterShowTimings_id = new_active_values.theatershowtimings = theater_show_timings_id.theatershowtimingsid
                    new_active_values.activeshowid = uuid.uuid4()
                    new_active_values.save()

                for itemtime in first_show_values:
                    theater_show_timings_id = TheaterShowTimings.objects.get(showname='first_show', showtime=itemtime)
                    new_active_values.MovieActiveDays_id = new_active_values.movieactivedays = movie_active_id.activedayid
                    new_active_values.TheaterShowTimings_id = new_active_values.theatershowtimings = theater_show_timings_id.theatershowtimingsid
                    new_active_values.activeshowid = uuid.uuid4()
                    new_active_values.save()

                for itemtime in second_show_values:
                    theater_show_timings_id = TheaterShowTimings.objects.get(showname='second_show', showtime=itemtime)
                    new_active_values.MovieActiveDays_id = new_active_values.movieactivedays = movie_active_id.activedayid
                    new_active_values.TheaterShowTimings_id = new_active_values.theatershowtimings = theater_show_timings_id.theatershowtimingsid
                    new_active_values.activeshowid = uuid.uuid4()
                    new_active_values.save()

            formstatus= "Done Bro"
    return render(request, 'Book/base_ticket_admin_area.html', {'formstatus': formstatus,
                                                                'forms': form,
                                                                'active_show_timings_list': active_show_timings_list,
                                                                'morning_show_values': morning_show_values,
                                                                })

# to match import re
# uuid4hex = re.compile('[0-9a-f]{32}\Z', re.I)
'''
How do I validate that a value is equal to the UUID4 generated by this code?

uuid.uuid4().hex
Should it be some regular expression? The values generated of 32-character-long strings of this form:

60e3bcbff6c1464b8aed5be0fce86052
'''