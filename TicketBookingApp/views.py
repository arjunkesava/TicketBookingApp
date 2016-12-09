from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    #return HttpResponse("Welcome to Main View of the TicketBooking App")
    return redirect('book/')