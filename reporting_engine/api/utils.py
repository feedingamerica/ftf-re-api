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
    d["Meta"] = dict()
    d["ReportInfo"] = []

    # Get ReportSchedule object of interest
    report_schedule = ReportSchedule.objects.get(pk=report_schedule_id)

    # Get startDate and endDate
    d["Meta"]["startDate"] = startDate
    d["Meta"]["endDate"] = endDate

    # Complete all fields in Meta
    d["Meta"]["scope_field"] = report_schedule.report_scope.field_reference
    d["Meta"]["scope_field_value"] = report_schedule.report_scope_value
    d["Meta"]["control_type_name"] = report_schedule.control_type.name
    d["Meta"]["control_age_group_id"] = report_schedule.control_age_group_id

    # Add all reports that reference the given ReportSchedule
    # TODO: Modify later for efficiency
    # https://docs.djangoproject.com/en/3.1/ref/models/relations/
    for dict_def in report_schedule.reporting_dictionary.reportingdictionarydefinition_set.all():
        report = dict()
        report["reportScheduleId"] = report_schedule.pk  # gets primary key of r
        report["reportDictId"] = dict_def.report_dictionary.pk  # common
        report["dataDefId"] = dict_def.data_definition.pk
        report["name"] = dict_def.data_definition.name
        report["dataDefType"] = dict_def.data_definition.data_definition_type.name
        d["ReportInfo"].append(report)

    for a in report_schedule.addin_reports.values_list('reporting_dictionary_id', flat = True):
        RD = ReportingDictionary(id=a, name=ReportingDictionary.objects.get(pk=a).name,
                                 definition=ReportingDictionary.objects.get(pk=a).definition)
        for dict_def in RD.reportingdictionarydefinition_set.all():
            report = dict()
            report["reportScheduleId"] = report_schedule.pk  # gets primary key of r
            report["reportDictId"] = dict_def.report_dictionary.pk  # common
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
