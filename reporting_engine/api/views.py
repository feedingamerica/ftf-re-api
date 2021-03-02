from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ReportScheduleSerializer
from api.models import ReportSchedule
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Specifies which method of API authentication this endpoint uses
@permission_classes([IsAuthenticated])          # IsAuthenticated class checks which auth method is used, and performs authentication based on that
def test_api_auth(request):
    """
    Endpoint specifically for testing if the Token Authentication works
    In the header of the GET request, make sure to supply Authorization as the key, and Token [token] as the value
    """
    return Response("Authentication Success!")
