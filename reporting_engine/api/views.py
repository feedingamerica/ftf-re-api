from django.shortcuts import render
from django.http import HttpResponse
from api.models import Report, ReportSchedule, RunType, TimeFrameType, ReportScope, ControlType, ReportingDictionary
from rest_framework import viewsets, permissions
from .serializers import ReportSerializer, ReportScheduleSerializer


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

# Create your views here.
