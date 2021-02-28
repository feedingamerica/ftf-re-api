from django.shortcuts import render
from django.http import HttpResponse
from api.models import Report, ReportSchedule, RunType, TimeFrameType, ReportScope, ControlType, ReportingDictionary
from rest_framework import viewsets, permissions
from .serializers import *


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
    queryset = TimeFrameType.objects.all()
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
