from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from serialize import report_schedule_serializer
from models import ReportSchedule

# Create your views here.

@api_view(['GET', 'POST'])
def report_schedule(request):
    if request.method == 'POST':
        #serialize input, within serializer determine if report exists
        serializer = report_schedule_serializer(data=request.data)
        #serializer.is_valid() should return true if report does not already exist
        if serializer.is_valid():
            serializer.save()
            #send data to functions to process report schedule
            return (serializer.data, status = status.HTTP_201_CREATED)
        return (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Got some data for new report schedule!", "data": request.data})
    else:
        #to be filled in later
        return Response({"message": "GET request to report schedule"})
