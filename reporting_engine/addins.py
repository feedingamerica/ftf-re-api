from api.models import ReportSchedule, ReportScope, AddinManager
import json
from django.core.serializers.json import DjangoJSONEncoder
from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections


#Questions
#report schedule model should the report scope value be a char
#do we have to be able to handle input that isnt present in the db 

#get object if exist in model else return none
def get_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  #if nothing matches return None
        obj = AddinManager(reporting_dictionary_id = None)
    return obj

def addin_helper(report_schedule_row):
    report_scope_id = report_schedule_row.report_scope_id
    report_scope_value = report_schedule_row.report_scope_value
    if(report_scope_id<9):
        field_reference=ReportScope.objects.get(pk=report_scope_id).field_reference #getting the field reference
        query=("SELECT dh.fb_id, dh.state_id FROM dim_hierarchies dh WHERE %s = %s LIMIT 1" % (field_reference, report_scope_value))
        conn=connections['source_db']
        dim_hier=pd.read_sql(query, conn)
        #if the report scope is 6 we only need to set the state
        if(report_scope_id!=6):
            fb_addin = get_or_none(AddinManager, report_scope_id=5,report_scope_value=dim_hier.fb_id)
            report_schedule_row.addin_foodbank_report_id=fb_addin.reporting_dictionary_id
        state_addin =  get_or_none(AddinManager, report_scope_id=6, report_scope_value= dim_hier.state_id)
        report_schedule_row.addin_state_report_id=state_addin.reporting_dictionary_id
    report_schedule_row.save()


def main():
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=3, report_scope_value= "2",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()
    print(rs.addin_foodbank_report_id, rs.addin_state_report_id)
    addin_helper(rs)
    print(rs.addin_foodbank_report_id, rs.addin_state_report_id)

if __name__ == "__main__":
    main()



def otherTests():
    #normal test
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=3, report_scope_value= "2",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()

    #report scope id == 9 nothing should be set
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=9, report_scope_value= "2",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()

    #report scope id > 9 nothing should be set
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=3, report_scope_value= "2",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()

    # report scope id == 6 ohio
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=6, report_scope_value= "39",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()

    # report scope id == 6 virgina
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=6, report_scope_value= "51",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()

    # report scope id == 5 MOFC
    ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=5, report_scope_value= "21",control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25").save()
    rs = ReportSchedule.objects.first()
