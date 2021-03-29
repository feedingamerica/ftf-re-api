from api.models import ReportSchedule, Report, ReportingDictionary
import json
from django.core.serializers.json import DjangoJSONEncoder


def get_data_definitions(report_schedule_id, startDate, endDate):
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
    d["Scope"]["startDate"] = startDate
    d["Scope"]["endDate"] = endDate

    # Complete all fields in Scope
    d["Scope"]["scope_field"] = report_schedule.report_scope.field_reference
    d["Scope"]["scope_field_value"] = report_schedule.report_scope_value
    d["Scope"]["control_type_name"] = report_schedule.control_type.name
    d["Scope"]["control_age_group_id"] = report_schedule.control_age_group_id

    # Add all reports that reference the given ReportSchedule
    # TODO: Modify later for efficiency
    # https://docs.djangoproject.com/en/3.1/ref/models/relations/
    for dict_def in report_schedule.reporting_dictionary.reportingdictionarydefinition_set.all():
        report = dict()
        report["reportScheduleId"] = report_schedule.pk  # gets primary key of r
        report["reportDictId"] = dict_def.reporting_dictionary.pk  # common
        report["dataDefId"] = dict_def.data_definition.pk
        report["name"] = dict_def.data_definition.name
        report["dataDefType"] = dict_def.data_definition.data_definition_type.name
        d["ReportInfo"].append(report)
    return d


def get_data_definitions_json(report_schedule_id):
    d = get_data_definitions(report_schedule_id)
    d = json.dumps(d, indent=4, cls=DjangoJSONEncoder)
    print(d)
    return d
