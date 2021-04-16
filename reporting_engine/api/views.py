from django.http import HttpResponse
from .models import Report, ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from .tasks import one_time_report_generation
from datetime import datetime
from addins import addin_helper
import pandas as pd
from django.db import connections
from pandas.core.frame import DataFrame
import json
from django.http import JsonResponse
from api.endpointreport import report_total

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
            # checking that the requested POST is a unique report schedule
            duplicate_schedule_serializer = self.serializer_class.check_uniqueness(schedule_serializer)

            # if the report is unique
            if (not(duplicate_schedule_serializer)):
                schedule = schedule_serializer.save()

                # generating any necessary addins for this schedule
                addin_helper(schedule)

                # if the schedule is "One Time", scheduling it to generate a report ASAP
                if (schedule.run_type.name == "One Time"):
                    one_time_report_generation.delay(schedule.id)

                # send data to functions to process report schedule
                return Response(schedule_serializer.data, status=status.HTTP_201_CREATED)
            return Response(duplicate_schedule_serializer.data, status=status.HTTP_208_ALREADY_REPORTED)
        return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# this gets a list of reports
@api_view(['GET'])
def get_reports(request, report_scope_id, report_scope_value):
    # getting the report's fields (note that all of these are optional report schedule parameters)
    control_type = request.GET.get('control_type')
    run_type = request.GET.get('run_type')
    timeframe_type = request.GET.get('timeframe_type')
    reporting_dictionary = request.GET.get('reporting_dictionary')
    control_age_group_id = request.GET.get('control_age_group_id')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    # getting all reports that match the given report scope id and value (these are the required report schedule parameters)
    reports = Report.objects.filter(report_schedule__report_scope_id = report_scope_id,
                                    report_schedule__report_scope_value = report_scope_value)

    # further filtering the reports list on all of the optional parameters, if they are present
    if (control_type):
        reports = reports.filter(report_schedule__control_type_id=control_type)
    if (run_type):
        reports = reports.filter(report_schedule__run_type_id=run_type)
    if (timeframe_type):
        reports = reports.filter(report_schedule__timeframe_type_id=timeframe_type)
    if (reporting_dictionary):
        reports = reports.filter(report_schedule__reporting_dictionary_id=reporting_dictionary)
    if (control_age_group_id):
        reports = reports.filter(report_schedule__control_age_group_id=control_age_group_id)
    if (start and end):
        reports = reports.filter(start_date = start)
        reports = reports.filter(end_date = end)
    # if given the start date but not end date, look at all start dates that are later or equal to the given
    elif(start):
        reports = reports.filter(start_date__gte = start)
    # if given the end date but not start date, look at all end dates that are before or equal to the given
    elif (end):
        reports = reports.filter(end_date__lte = end)

    # displaying the filtered list
    serializer = ReportSerializer(reports, many=True)

    return Response(serializer.data)

#this gets all the options for a report
@api_view(['GET'])
def report_options(request):
    #get all distinct dim_ages and use pandas to format it into json
    query= "select distinct age_grouping_id, age_grouping_name, start_age, end_age, age_band_name_to from source_beta.dim_ages" 
    conn=connections['source_db']
    dim_ages=pd.read_sql(query, conn).reset_index().to_json(orient='records')
    dim_ages = json.loads(dim_ages)
    #get name and id for run_types, timeframe_types, report_scopes, control_types and reporting_dictionary
    run_types = RunType.objects.values("id", "name")
    timeframe_type = TimeframeType.objects.values("id", "name")
    report_scopes = ReportScope.objects.values("id", "name")
    control_type = ControlType.objects.values("id", "name")
    reporting_dict  = ReportingDictionary.objects.values("id", "name")
    #convert result to json
    qs_json = JsonResponse({'reporting_dict': list(reporting_dict), 'control_type': list(control_type), "report_scopes":list(report_scopes), "timeframe_type":list(timeframe_type), "run_types": list(run_types), "dim_ages": dim_ages}, safe = False)
    return qs_json

#this gets a specific report given a report_id
@api_view(['GET'])	
def get_report_total(request, report_id):
    report_json = report_total(report_id)
    return report_json