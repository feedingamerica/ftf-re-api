from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ReportScheduleSerializer
from api.models import ReportSchedule

# Create your views here.

@api_view(['GET', 'POST'])
def report_schedule(request):
    if request.method == 'POST':
        #serialize input, within serializer determine if report exists
        serializer = ReportScheduleSerializer(data=request.data)
        #serializer.is_valid() should return true if report does not already exist
        if serializer.is_valid():
            serializer.save()
            #send data to functions to process report schedule
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        report_schedules = ReportSchedule.objects.all()
        serializer = ReportScheduleSerializer(report_schedules, many=True)
        #to be filled in later
        return Response(serializer.data)
