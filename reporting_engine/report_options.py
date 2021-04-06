from api.models import RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary
import pandas as pd
from django.db import connections
from django.core import serializers
from pandas.core.frame import DataFrame
import json
from django.http import JsonResponse


def report_options(request):
	if request.method != 'GET'
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
	