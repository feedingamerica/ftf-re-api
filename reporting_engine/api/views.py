from django.shortcuts import render
from django.views import View

# Create your views here.


def report_schedule(request):
    if request.method == 'POST':
        #serialize input
        data = request.data
        #send data to functions to process report schedule
    else:
        #to be filled in later
        return (1)
    return (1)