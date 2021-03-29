from django.http import HttpResponse
from .models import Report, ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from .tasks import one_time_report_generation

class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Report table
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']


class RunTypeViewSet(viewsets.ModelViewSet):
    queryset = RunType.objects.all()
    serializer_class = RunTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']

class TimeframeTypeViewSet(viewsets.ModelViewSet):
    queryset = TimeframeType.objects.all()
    serializer_class = TimeframeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']


class ReportScopeViewSet(viewsets.ModelViewSet):
    queryset = ReportScope.objects.all()
    serializer_class = ReportScopeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']


class ControlTypeViewSet(viewsets.ModelViewSet):
    queryset = ControlType.objects.all()
    serializer_class = ControlTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']


class ReportingDictionaryViewSet(viewsets.ModelViewSet):
    queryset = ReportingDictionary.objects.all()
    serializer_class = ReportingDictionarySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names=['get']

class ReportScheduleViewSet(viewsets.ModelViewSet):
    queryset = ReportSchedule.objects.all()
    serializer_class = ReportScheduleSerializer
    http_method_names=['get', 'post']
    # permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        schedule_serializer = self.serializer_class(data=request.data)
        if schedule_serializer.is_valid():
            #uniqueness = self.serializer_class.check_uniqueness(schedule_serializer, data=request.data)
            duplicate_schedule_serializer = self.serializer_class.check_uniqueness(schedule_serializer)
            if (not(duplicate_schedule_serializer)):
            #if (duplicate_schedule_serializer == 0):
                schedule = schedule_serializer.save()
                if (schedule.run_type.name == "One Time"):
                    one_time_report_generation.delay(schedule.id)
                # send data to functions to process report schedule
                return Response(schedule_serializer.data, status=status.HTTP_201_CREATED)
            return Response(duplicate_schedule_serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
