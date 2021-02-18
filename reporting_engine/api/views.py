from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
from rest_framework import viewsets, permissions
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Report table
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
