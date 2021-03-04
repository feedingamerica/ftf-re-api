from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework_api_key.permissions import HasAPIKey
from api.serializers import ReportScheduleSerializer
from api.models import ReportSchedule

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([HasAPIKey])
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
@permission_classes([HasAPIKey])
def test_api_key(request):
    """
    Endpoint for testing if API Key authentication works
    In the header of the GET request, make sure to supply "X-Api-Key" as the key, and your api key as the value.
    """
    #return Response("You are authorized to access this endpoint!")
    return Response("test_api_key worked")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([HasAPIKey & IsAdminUser])
def test_api_key_and_auth(request):
    """
    Endpoint to demonstrate limiting access to only those with API Key's and who have admin tokens. Use this for admin only endpoints.
    In the header of the GET request, supply the following two key value pairs:
    "Authorization": "Token [token]",
    "X-Api-Key": "[your api key here]"
    """
    return Response("test_api_key_and_auth worked")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([HasAPIKey | IsAdminUser])
def test_api_key_or_auth(request):
    """
    Endpoint to demonstrate allowing access with either an API key or an admin Token.
    In the header of the GET request, supply either of the following two key value pairs:
    "Authorization": "Token [token]",
    "X-Api-Key": "[your api key here]"
    """
    return Response("test_api_key_or_auth worked")