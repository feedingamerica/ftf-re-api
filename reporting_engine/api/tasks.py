from celery import shared_task
from api.models import ReportSchedule
from transform_layer.calculations import CalculationDispatcher

@shared_task
def test():
    print("hi")

@shared_task
def periodic_report_generation():
    for schedule in ReportSchedule.objects.all():
        # make sure this works:
        print(f'Report Schedule: ID - {schedule.id}, Date Scheduled - {schedule.date_scheduled}')
        
        # in future, will be calling some functions to actually generate reports
        # these aren't built yet, but could be something like the below...
        # dictionary = get_dictionary(schedule.id)
        # results = call_transformation_layer(dictionary)
        # cd = CalculationDispatcher(dictionary)
        # results = cd.run_calculations()
