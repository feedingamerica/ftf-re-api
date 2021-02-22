from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view

# Create your views here.

@api_view()
def report_schedule(request):
    if request.method == 'POST':
        #serialize input
        data = request.data
        #send data to functions to process report schedule
        return Response({"message": "Got some data for new report schedule!", "data": request.data})
    else:
        #to be filled in later
        return Response({"message": "GET request to report schedule"})
