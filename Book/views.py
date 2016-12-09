from django.http import Http404
from django.shortcuts import render
from .models import UserDetails, MovieDetails, TheaterBase, SeatingTable, BookedRecords, TheaterShowTimings, MovieActiveDays
import time
import json
from datetime import datetime, timedelta
from django.core import serializers

# The Notes link is https://shrib.com/9gzBoNbh8HIrnqC
def index(request):
    #### Active Dates Data
    current_date = time.strftime("%Y-%m-%d")
    end_date = datetime.now() + timedelta(days=7)
    end_date = end_date.strftime("%Y-%m-%d")
    active_dates_content = MovieActiveDays.objects.filter(showfromdate__lte=current_date, showenddate__gte=end_date).distinct()

    today_movies_list = MovieDetails.objects.filter(movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date).distinct()
    today_movies_list_names = MovieDetails.objects.filter(movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date).distinct().values_list('movieid', 'moviename')
    today_theater_list_names = TheaterBase.objects.filter(movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date).distinct()

    ## Array to print current + 6 days
    weeklist = []
    for x in range(0, 6):
        weeklist.append(datetime.now() + timedelta(days=x))


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
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'weeklist': weeklist,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'selected_moviename': 'Select Movie Name',
                                                                  'selected_theatername': 'Select Theater Name',
                                                                  'selected_showdate': 'Select Date',
                                                                  'selected_showname': 'Select Show Time',
                                                                  })

def movie(request, url_movie_id):
    try:
        url_movie_id = int(url_movie_id)
    except ValueError:
        raise Http404()

    request.session['selected_moviename_id'] = url_movie_id
    if url_movie_id:
        movie_details = MovieDetails.objects.filter(movieid=url_movie_id)
        selected_moviename = MovieDetails.objects.get(movieid=url_movie_id).moviename
        request.session['selected_moviename'] = selected_moviename
    else:       # if url movieid is null
        movie_details = MovieDetails.objects.all().values('moviename')
        request.session['selected_moviename'] = 'Select Movie Name'

    current_date = request.session.get('current_date')
    end_date = request.session.get('end_date')

    today_movies_list_names = MovieDetails.objects.filter(movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date).values_list('movieid', 'moviename').distinct()
    if request.session.get('selected_moviename') != 'Select Movie Name':
        today_theater_list_names = TheaterBase.objects.filter(movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date, movieactivedays__moviedetails=url_movie_id).distinct()
        weeklist = []
        for x in range(0, 6):
            showdate = datetime.now() + timedelta(days=x)
            if bool(MovieDetails.objects.filter(movieactivedays__showfromdate__lte=showdate, movieactivedays__showenddate__gte=showdate, movieid=url_movie_id).values_list('movieid', 'moviename').distinct().exists()) :
                weeklist.append(showdate)

    return render(request, 'Book/base_active_area_content.html', {'today_movies_list': movie_details,
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'selected_moviename': selected_moviename,
                                                                  'weeklist': weeklist,
                                                                  'selected_theatername': 'Select Theater Name',
                                                                  'selected_showdate': 'Select Date',
                                                                  'selected_showname': 'Select Show Time',
                                                                  })

def theater(request, theaterid):
    try:
        theaterid = int(theaterid)
    except ValueError:
        raise Http404()

    current_date = request.session.get('current_date')
    request.session['selected_theatername_id'] = theaterid





    #if request.session.get('selected_theatername') == 'Select Theater Name':
    #    request.session['selected_theatername'] = TheaterBase.objects.get(theaterid=theaterid).theatername
    theater_filter_value = 'movieactivedays__theaterbase'
    fromdate_filter_value = 'movieactivedays__showfromdate__lte'
    enddate_filter_value = 'movieactivedays__showenddate__gte'

    today_movies_list = MovieDetails.objects.filter(
        **{theater_filter_value: request.session.get('selected_theatername_id'), fromdate_filter_value: current_date,
           enddate_filter_value: current_date}).distinct()
    today_theater_list_names = TheaterBase.objects.all().values('theatername').distinct()
    today_movies_list_names = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid, movieactivedays__showfromdate__lte=current_date, movieactivedays__showenddate__gte=current_date).values_list('movieid', 'moviename').distinct()

    #active_dates_content = MovieActiveDays.objects.filter(showfromdate__lte=current_date, showenddate__gte=end_date, theaterbase=theaterid)


    return render(request, 'Book/base_active_area_content.html', {'today_movies_list': today_movies_list,
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'selected_moviename': 'Select a Movie',
                                                                  'selected_theatername': request.session.get('selected_theatername'),
                                                                  'selected_showdate': 'Select Date',
                                                                  'selected_showname': 'Select Show Time',
                                                                  })

def date(request, url_showdate):
    date_i_got = url_showdate

    request.session['selected_date'] = url_showdate

    current_date = request.session.get('current_date')
    if request.session.get('selected_moviename') == 'Select Movie Name':

        if request.session.get('selected_theatername') == 'Select Theater Name':

            if request.session.get('selected_showname') == 'Select Show Time':

                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                                movieactivedays__showfromdate__lte=current_date,
                                                                movieactivedays__showenddate__gte=current_date).distinct()
            else:
                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                                movieactivedays__showfromdate__lte=current_date,
                                                                movieactivedays__showenddate__gte=current_date).distinct()
        else:
            selected_date = request.session.get('selected_showdate')
            today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                            movieactivedays__showfromdate__lte=selected_date,
                                                            movieactivedays__showenddate__gte=selected_date).distinct()
    else:
        today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                        movieactivedays__showfromdate__lte=current_date,
                                                        movieactivedays__showenddate__gte=current_date,
                                                        movieactivedays__movieid=request.session.get(
                                                            'selected_moviename_id')).distinct()

    today_movies_list = MovieDetails.objects.filter(movieactivedays__showfromdate__lte=date_i_got, movieactivedays__showenddate__gte=date_i_got).distinct()
    today_movies_list_names = MovieDetails.objects.filter(movieactivedays__showfromdate__lte=date_i_got, movieactivedays__showenddate__gte=date_i_got).values_list('movieid', 'moviename').distinct()
    today_theater_list_names = TheaterBase.objects.all()

    return render(request, 'Book/base_active_area_content.html', {'today_movies_list': today_movies_list,
                                                                  #'session_check': request.session.get('session_movies_list'),
                                                                  'today_movies_list_names': today_movies_list_names,
                                                                  'selected_moviename': 'Select a Movie',
                                                                  'today_theater_list_names': today_theater_list_names,
                                                                  'selected_theatername': 'Select a Theater',
                                                                  'selected_showdate': date_i_got,
                                                                  'selected_showname': 'Select Show Time',
                                                                  })


'''
    if request.session.get('selected_moviename') == 'Select Movie Name':

        if request.session.get('selected_showdate') == 'Select Date':

            if request.session.get('selected_showname') == 'Select Show Time':

                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                                movieactivedays__showfromdate__lte=current_date,
                                                                movieactivedays__showenddate__gte=current_date).distinct()
            else:
                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                                movieactivedays__showfromdate__lte=current_date,
                                                                movieactivedays__showenddate__gte=current_date).distinct()
        else:
            selected_date = request.session.get('selected_showdate')
            today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                            movieactivedays__showfromdate__lte=selected_date,
                                                            movieactivedays__showenddate__gte=selected_date).distinct()
    else:

        if request.session.get('selected_showdate') == 'Select Date':

            if request.session.get('selected_showname') == 'Select Show Time':

                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                        movieactivedays__showfromdate__lte=current_date,
                                                        movieactivedays__showenddate__gte=current_date,
                                                        movieactivedays__movieid=request.session.get('selected_moviename_id')).distinct()
            else:

                today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                                movieactivedays__showfromdate__lte=current_date,
                                                                movieactivedays__showenddate__gte=current_date,
                                                                movieactivedays__movieid=request.session.get('selected_moviename_id')).distinct()
        else:

            selected_date = request.session.get('selected_showdate')
            today_movies_list = MovieDetails.objects.filter(movieactivedays__theaterbase=theaterid,
                                                            movieactivedays__showfromdate__lte=selected_date,
                                                            movieactivedays__showenddate__gte=selected_date,
                                                            movieactivedays__movieid=request.session.get(
                                                                'selected_moviename_id')).distinct()
'''