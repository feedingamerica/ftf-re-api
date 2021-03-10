from celery import shared_task
from api.models import ReportSchedule, Report, ReportDataInt, ReportDataFloat
from datetime import date

@shared_task
def test():
    print("hi")

@shared_task
def periodic_report_generation():
    for schedule in ReportSchedule.objects.all():
        # make sure this works:
        print(schedule.id)
        print(schedule.date_scheduled)
        
        # in future, will be calling some functions to actually generate reports
        # these aren't built yet, but could be something like the below...
        # dictionary = get_dictionary(schedule.id)
        # results = call_transformation_layer(dictionary)
        # save_report(schedule, reports)

def save_report(schedule, results):
    # New report to the report
    dateCompleted = date.today().strftime('%Y-%m-%d')
    new_report = Report(report_schedule = schedule, start_date = results['Scope']['startDate'], end_date = results['Scope']['endDate'], date_completed = dateCompleted)
    new_report.save()

    #New rows to report_data_int
    for values in results['ReportInfo']:
        if(values['dataDefType'] == 'integer'):
            new_data_int = ReportDataInt(report = new_report, data_definition_id = values['dataDefId'], int_value = values['value'])
            new_data_int.save()
        elif(values['dataDefType'] == 'float'):
            new_data_float = ReportDataFloat(report = new_report, data_definition_id = values['dataDefId'], float_value = values['value'])
            new_data_float.save()

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
			'reportId': 1,
			'reportDictId': 1,
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