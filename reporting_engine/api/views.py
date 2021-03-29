from django.http import HttpResponse
from api.models import Report, ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.decorators import api_view


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Report table
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportScheduleViewSet(viewsets.ModelViewSet):
    queryset = ReportSchedule.objects.all()
    serializer_class = ReportScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class RunTypeViewSet(viewsets.ModelViewSet):
    queryset = RunType.objects.all()
    serializer_class = RunTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TimeFrameTypeViewSet(viewsets.ModelViewSet):
    queryset = TimeframeType.objects.all()
    serializer_class = TimeFrameTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportScopeViewSet(viewsets.ModelViewSet):
    queryset = ReportScope.objects.all()
    serializer_class = ReportScopeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ControlTypeViewSet(viewsets.ModelViewSet):
    queryset = ControlType.objects.all()
    serializer_class = ControlTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportingDictionaryViewSet(viewsets.ModelViewSet):
    queryset = ReportingDictionary.objects.all()
    serializer_class = ReportingDictionarySerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.


@api_view(['GET', 'POST'])
def report_schedule(request):
    if request.method == 'POST':
        # serialize input, within serializer determine if report exists
        serializer = ReportScheduleSerializer(data=request.data)
        # serializer.is_valid() should return true if report does not already exist
        if serializer.is_valid():
            serializer.save()
            # send data to functions to process report schedule
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        report_schedules = ReportSchedule.objects.all()
        serializer = ReportScheduleSerializer(report_schedules, many=True)
        # to be filled in later
        return Response(serializer.data)
