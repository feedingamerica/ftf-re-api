from celery import shared_task
from .utils import get_data_definitions
from transform_layer.calculations import CalculationDispatcher
from .models import ReportSchedule, Report, ReportDataInt, ReportDataFloat, ReportDataJson
import datetime
from datetime import date, timedelta
import json

# calculates report parameters, generates the report, and saves it to the reports database
def generate_report_and_save(schedule):      
    # get the start and end date that defines the timeframe the report should be run for
    start_date, end_date = calculate_dates(schedule)

    # get data definitions for current schedule and perform necessary calculations to generate the report
    data_def_dict = get_data_definitions(schedule.id, start_date, end_date)

    cd = CalculationDispatcher(data_def_dict)
    cd.run_calculations()

    # save the generated report to the database
    save_report(schedule, data_def_dict)

# calculates start and end dates that a report should be run for, based on its timeframe type
def calculate_dates(schedule): 
    # the end date is the same for all timeframes except custom: the last day of the previous month
    end_date = schedule.date_scheduled.replace(day = 1) - timedelta(days = 1)
 
    # calculating start date based on timeframe type
    if (schedule.timeframe_type.name == "Last Month"):
        # first day of previous month
        start_date = datetime.date(end_date.year, end_date.month, 1)
    elif (schedule.timeframe_type.name == "Rolling 12 Months"):
        # first day of the same month, previous year
        start_date = datetime.date(schedule.date_scheduled.year - 1, schedule.date_scheduled.month, 1)
    elif (schedule.timeframe_type.name == "CY To Date"):
        # January 1 of this year
        start_date = datetime.date(end_date.year, 1, 1)
    elif (schedule.timeframe_type.name == "Fiscal year to date"):
        # July 1 of the previous year
        start_date = datetime.date(end_date.year - 1, 7, 1)
    elif (schedule.timeframe_type.name == "Custom Date Range"):
        # these custom dates are stored in the report_schedules table 
        start_date = schedule.date_custom_start
        end_date = schedule.date_custom_end
        
    # convert datetime objects to string
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    return start_date, end_date

@shared_task
def test_task(param):
    print(param)
    print("Test task executed correctly.")

# generates (and saves) recurring reports if they are due based on recurrence parameter
@shared_task
def periodic_report_generation(recurrence):
    for schedule in ReportSchedule.objects.all():
	    if (schedule.timeframe_type.recurrence_type == recurrence):
		    generate_report_and_save(schedule)


# generates (and saves) a one-time report if it has been requested
@shared_task
def one_time_report_generation(schedule_id):
	schedule = ReportSchedule.objects.get(id=schedule_id)
	print(f"Testing execution of one off report generation for {schedule.id}...")
	generate_report_and_save(schedule)

# saves the given calculated report to the reports database
def save_report(schedule, results):
    # New report to the database
    dateCompleted = date.today().strftime('%Y-%m-%d')

    # checking if no_data is in the Meta dict of results
    # this should always be there, but just in case a new data definition has been added but not taken into account when checking for data,
    # or something else happens, checking for that field before using it to populate the new Report
    if 'no_data' in results['Meta']:
        new_report = Report(report_schedule = schedule, start_date = results['Meta']['startDate'], end_date = results['Meta']['endDate'], date_completed = dateCompleted, no_data = results['Meta']['no_data'])
    else:
        new_report = Report(report_schedule = schedule, start_date = results['Meta']['startDate'], end_date = results['Meta']['endDate'], date_completed = dateCompleted)
    
    # saving report to the database
    new_report.save()

    # New rows to report_data_int/report_data_float, if there are calculated values for this report
    if ('no_data' in results['Meta'] and results['Meta']['no_data'] == False):
        for values in results['ReportInfo']:
            if(values['dataDefType'] == 'integer'):
                new_data_int = ReportDataInt(report = new_report, data_definition_id = values['dataDefId'], int_value = values['value'])
                new_data_int.save()
            elif(values['dataDefType'] == 'float'):
                new_data_float = ReportDataFloat(report = new_report, data_definition_id = values['dataDefId'], float_value = values['value'])
                new_data_float.save()
            elif(values['dataDefType'] == 'json'):
                new_data_json = ReportDataJson(report = new_report, data_definition_id = values['dataDefId'], json_object = json.loads(values['value']))
                new_data_json.save()
    

# used for testing purposes
mock_dict = {
    'Scope':  {
        'startDate': '2019-01-01',
        'endDate': '2019-12-31',
        'scope_type': 'hierarchy',
        'scope_field': 'fb_id',
        'scope_field_value': 21,
        'control_type_field': 'dummy_is_grocery_service',
        'control_type_value': 1
    },
    'ReportInfo': [
        {
            'reportId': 1,
            'reportDictId': 1, 
            'dataDefId': 1,
            'dataDefType': 'integer',
            'name': 'services_total',
            'value': 1040876
        }, 
        {
            'reportId': 1, 'reportDictId': 1,
            'dataDefId': 2,
            'dataDefType': 'integer',
            'name': 'undup_hh_total',
            'value': 161114
        },
        {
            'reportId': 1,
            'reportDictId': 1,
            'dataDefId': 2,
            'dataDefType': 'float',
            'name': 'undup_hh_total',
            'value': 1.507
        }
    ]
}
