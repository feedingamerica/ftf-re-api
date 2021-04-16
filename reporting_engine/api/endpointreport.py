"""
endpointreport.py

This file contains the function report_total, which takes in a report_id and returns a report in
json format. 

This script cannot be executed directly from the command line. The code must be copied and pasted
into Django's shell or it must be imported into another script. 

Written by Joy Lin, Nick Biederman, Alli Hornyak, and Emily Robinson
"""
from api.models import ReportScope, ReportingDictionary, Report,  ReportSchedule, ReportScheduleAddin, ReportingDictionaryDefinition 
from api.models import DataDefinition, DataDefinitionType, ReportingDictionarySection, ReportScheduleAddinReport
from api.models import ReportDataInt, ReportDataFloat, ReportDataJson
import pandas as pd
from django.db import connections
from pandas.core.frame import DataFrame
import json
from django.http import JsonResponse
from django.apps import apps

def report_total(report_id):
    bn = {}
    data = {}
    total = {}
    report_dict_id = list()
    section_list = list()
    type_object = None
    #get report_schedule_id using report_id
    report_sch_id = Report.objects.get(pk = report_id).report_schedule_id
    #get the report_schedule object that matches the report_schedule_id
    schedule_items = ReportSchedule.objects.get(pk = report_sch_id)
    #get the report object that matches the report_id
    report_items = Report.objects.get(pk = report_id)
    #construct the 'meta' part of the json response
    meta = {'report_id' :report_id, 'report_schedule_id': report_sch_id,'run_type_id':schedule_items.run_type_id, 'report_scope_id': schedule_items.report_scope_id , 
			'report_scope_value': schedule_items.report_scope_value, 'control_type_id': schedule_items.control_type_id, 
			'reporting_dictionary_id': schedule_items.reporting_dictionary_id, 'control_age_group_id': schedule_items.control_age_group_id,'date_scheduled': schedule_items.date_scheduled,  
			'start_date': report_items.start_date, 'end_date': report_items.end_date, 'date_completed': report_items.date_completed, 'no_data': report_items.no_data}
    #append the reporting_dictionary_id specific to this report_schedule into a list 
    report_dict_id.append(schedule_items.reporting_dictionary_id)
    #find the list of addins for this report_schedule
    re_sch_addin_id = ReportScheduleAddinReport.objects.filter(report_schedule_id = report_sch_id).values_list("report_schedule_addin_id", flat = True)
    for item in re_sch_addin_id:
            #append reporting_dictionary_id for addins to the list of reporting_dictionary_ids
            report_dict_id.append(ReportScheduleAddin.objects.get(pk = item).reporting_dictionary_id)
    #go through each reporting_dictionary_id to fill out the 'data' section
    for item in report_dict_id:
        #get a distict list of section related to the reporting_dictionary_id
        sect_id = ReportingDictionaryDefinition.objects.filter(report_dictionary_id = item).values("section_id").distinct()
        #run through each section_id to get name of section, data_definition names and data
        for value in sect_id:
            #get section name
            names=ReportingDictionarySection.objects.get(pk=value['section_id']).name
            #get the queryset of objects that is in a the section
            rep_dict_def_items = ReportingDictionaryDefinition.objects.filter(report_dictionary_id = item, section_id = value['section_id'])
            for idx in rep_dict_def_items:
                #get data_definition object
                temp = DataDefinition.objects.get(pk = idx.data_definition_id)
                #get data_definition_type
                data_definition_type_id = temp.data_definition_type_id
                #store the data_definition anem into json
                bn[temp.name] = {}
                #using report_id and data_definition_type_id find the table that stores the information and load it in
                if data_definition_type_id == 1:
                    try:
                        type_object = ReportDataInt.objects.get( data_definition = idx.data_definition_id, report_id = report_id).int_value
                    except ReportDataInt.DoesNotExist:
                        #return empty if nothing matches
                        type_object = {}
                elif data_definition_type_id == 2:
                    try:
                        type_object = ReportDataJson.objects.get( data_definition = idx.data_definition_id, report_id = report_id).json_object
                    except ReportDataJson.DoesNotExist:
                        #return empty if nothing matches
                        type_object = {}
            
                elif data_definition_type_id == 3:
                    try:
                        type_object = ReportDataFloat.objects.get( data_definition = idx.data_definition_id, report_id = report_id).float_value
                    except ReportDataFloat.DoesNotExist:
                        #return empty if nothing matches
                        type_object = {}
                else:
                    return "Data Definition Type Incorrect"
                #retun empty if value is none
                if type_object is None:
                    type_object = {}
                #store the data with their data_definition name
                bn[temp.name] = type_object
            #store all data_definitions into the each section
            data[names] = bn
            #clear bn
            bn = {}
    #put the meta and data part together and convert it to Json
    total["meta"] = meta
    total["data"] = data
    qs_json = JsonResponse(total)
    #return json
    return qs_json
