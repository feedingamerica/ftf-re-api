from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ReportScheduleSerializer
from api.models import ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary
from endpointreport import report_total
import pandas as pd
from django.db import connections
from django.core import serializers
from pandas.core.frame import DataFrame
import json
from django.http import JsonResponse

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


def report_options(request):
    if request.method != 'GET':
        Exception("Expected GET; recived " + request.method)
	query= "select distinct age_grouping_id, age_grouping_name, start_age, end_age, age_band_name_to from source_beta.dim_ages" 
	conn=connections['source_db']
	dim_ages=pd.read_sql(query, conn)
	run_types = RunType.objects.values("id", "name")
	timeframe_type = TimeframeType.objects.values("id", "name")
	report_scopes = ReportScope.objects.values("id", "name")
	control_type = ControlType.objects.values("id", "name")
	reporting_dict  = ReportingDictionary.objects.values("id", "name")
	qs_json = JsonResponse({'reporting_dict': list(reporting_dict), 'control_type': list(control_type), "report_scopes":list(report_scopes), "timeframe_type":list(timeframe_type), "run_types": list(run_types), "dim_ages": dim_ages.values.tolist()}, safe = False)
	return qs_json
