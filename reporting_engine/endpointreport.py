from api.models import ReportScope, ReportingDictionary, Report,  ReportSchedule, ReportScheduleAddin, ReportingDictionaryDefinition 
from api.models import DataDefinition, DataDefinitionType, ReportingDictionarySection, ReportScheduleAddinReport
from api.models import ReportDataInt, ReportDataFloat, ReportDataJson
import pandas as pd
from django.db import connections
from django.core import serializers
from pandas.core.frame import DataFrame
import json
from django.http import JsonResponse
from django.apps import apps

	
def report_total(request, report_id):
    bn={}
    data={}
    report_dict_id= list()
    section_list=list()
    type_object=None
    report_sch_id=Report.objects.get(pk=report_id).report_schedule_id
    schedule_items=ReportSchedule.objects.get(pk=report_sch_id)
    report_items = Report.objects.get(pk=report_id)
    meta = {' report_id' :report_id, "report_schedule_id": report_sch_id,"run_type_id":schedule_items.run_type_id, "report_scope_id": schedule_items.report_scope_id , 
			'report_scope_value': schedule_items.report_scope_value, 'control_type_id': schedule_items.control_type_id, 
			'reporting_dictionary_id': schedule_items.reporting_dictionary_id, 'control_age_group_id': schedule_items.control_age_group_id, 'date_scheduled': schedule_items.date_scheduled,  
			"start_date": report_items.start_date, 'end_date': report_items.end_date, "date_completed": report_items.date_completed} 
    #print(meta)
    report_dict_id.append(schedule_items.reporting_dictionary_id)
    re_sch_addin_id = ReportScheduleAddinReport.objects.filter(report_schedule_id= report_sch_id).values_list("report_schedule_addin_id", flat=True)
    #print(re_sch_addin_id)
    for item in re_sch_addin_id:
            #print(item)
            report_dict_id.append(ReportScheduleAddin.objects.get(pk = item).reporting_dictionary_id)
    #print(report_dict_id)
    #addin_names= ReportingDictionary.objects.filter(pk = item).name)
    for item in report_dict_id:
        sect_id = ReportingDictionaryDefinition.objects.filter(report_dictionary_id=item).values("section_id").distinct()
        #print(sect_id)
        #print(item)
        for value in sect_id:           
                names=ReportingDictionarySection.objects.get(pk=value['section_id']).name
                #print(item)
                #print(value['section_id'])
                rep_dict_def_items = ReportingDictionaryDefinition.objects.filter(report_dictionary_id=item, section_id =value['section_id'] )
                for idx in rep_dict_def_items:
                    temp = DataDefinition.objects.get(pk = idx.data_definition_id)
                    data_definition_type_id= temp.data_definition_type_id
                    bn[temp.name]={}
                    if data_definition_type_id ==1:
                        try:
                            type_object=ReportDataInt.objects.get( data_definition = idx.data_definition_id, report_id = report_id).int_value
                        except ReportDataInt.DoesNotExist:
                            type_object={}
                    elif data_definition_type_id ==2:
                        try:
                            type_object=ReportDataJson.objects.get( data_definition = idx.data_definition_id, report_id = report_id).json_object
                        except ReportDataJson.DoesNotExist:
                            type_object={}
                
                    elif data_definition_type_id ==3:
                        try:
                            type_object=ReportDataFloat.objects.get( data_definition = idx.data_definition_id, report_id = report_id).float_value
                        except ReportDataFloat.DoesNotExist:
                            type_object={}
                
                    else:
                        return "ERROR MESSAGE"
                    bn[temp.name]=type_object
                    #print(names)
                data[names]=bn
                bn={}
    total={}
    total["meta"]=meta
    total["data"]=data
    qs_json = JsonResponse(total)
    #print(qs_json.content)
    return qs_json








