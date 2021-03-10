from api.models import ReportSchedule, ReportScope, AddinManager
import json
from django.core.serializers.json import DjangoJSONEncoder
from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections

def addin_manager(report_schedule_row):

   report_scope_id = report_schedule_row.report_scope_id
   print("_________")
   print(report_scope_id)
   if(report_scope_id>=9):
       report_schedule_row.addin_foodbank=None
       report_schedule_row.addin_state=None
   else:
       report_scope=ReportScope.objects.get(pk=report_scope_id) #getting tuple for report scope
       field_reference=report_scope.field_reference #getting the field reference, might need to typecast
       #query=("SELECT fb_id,state_id from dim_hierarchies where %s = 3" % (field_reference))
       query=("SELECT fb_id from dim_hierarchies")
       conn=connections["source_db"]
       print("____________")
       dim_hier=pd.read_sql(query,conn)
       print(dim_hier)
       fb=dim_hier[0]
       state=dim_hier[1]
       fb_addin = addin_manager.objects.get(report_scope_id=5,report_scope_value=fb)
       report_schedule_row.addin_foodbank=fb_addin.reporting_dictionary
       state_addin = addin_manager.objects.get(report_scope_id=6, report_scope_value=state)
       report_schedule_row.addin_state=state_addin.reporting_dictionary

       #if the report scope is 6 we only need to set the state

def main():
    rs = ReportSchedule.objects.all()
    print(rs[1])
    addin_manager(rs[1])
    print(rs[1])
    
if __name__ == "__main__":
    main()

rs = ReportSchedule(run_type_id=2, timeframe_type_id=2, report_scope_id=3, control_type_id=1, reporting_dictionary_id=1, control_age_group_id=1, date_scheduled="2021-02-25")