from api.models import ReportSchedule, Report
import json
from django.core.serializers.json import DjangoJSONEncoder


def get_data_definitions(report_schedule_id):
    """
    Takes a report schedule id and returns a dictionary/json
    of the necessary data definitions to be used by the
    transformation layer.
    """

    # Setup the dictionary/json object
    d = dict()
    d["Scope"] = dict()
    d["ReportInfo"] = []

    # Get ReportSchedule object of interest
    report_schedule = ReportSchedule.objects.get(pk=report_schedule_id)

    # Get startDate and endDate
    if report_schedule.run_type.name == "One Time":
        d["Scope"]["startDate"] = report_schedule.date_custom_start
        d["Scope"]["endDate"] = report_schedule.date_custom_end
    elif report_schedule.run_type.name == "Recurring":
        d["Scope"]["startDate"] = report_schedule.timeframe_type.current_start_date
        d["Scope"]["endDate"] = report_schedule.timeframe_type.current_end_date

    # Complete all fields in Scope
    d["Scope"]["scope_field"] = report_schedule.report_scope.field_reference
    d["Scope"]["scope_field_value"] = report_schedule.report_scope_value
    d["Scope"]["control_type_field"] = report_schedule.control_type.name
    d["Scope"]["control_type_value"] = 1  # For now this will always be 1

    # Add all reports that reference the given ReportSchedule
    # TODO: Modify later for efficiency
    # https://docs.djangoproject.com/en/3.1/ref/models/relations/
    for r in Report.objects.filter(report_schedule=report_schedule):
        report = dict()
        report["reportId"] = r.pk  # gets primary key of r
        report["reportDictId"] = report_schedule.reporting_dictionary.pk  # common
        report["dataDefId"] = None  # FIXME: Cannot be completed due to models
        report["name"] = "name"  # FIXME: currently no name in models
        d["ReportInfo"].append(report)

    return d


def get_data_definitions_json(report_schedule_id):
    d = get_data_definitions(report_schedule_id)
    d = json.dumps(d, indent=4, cls=DjangoJSONEncoder)
    print(d)
    return d
