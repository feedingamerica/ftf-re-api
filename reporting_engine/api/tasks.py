from celery import shared_task
from api.models import ReportSchedule

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
        # 
        # New report to the report
        # new_report = Report(report_schedule = schedule, start_date = results.scope.start_date, end_date = results.scope.end_date, date_completed = date.today())
        # new_report.save()
        #
        # New rows to report_data_int
        # for values in results.ReportInfo.objects.all():
        #   new_data_int = ReportDataInt(report = new_report, data_definition = values.dataDefId, int_value = values.value)
        #   new_data_int.save()