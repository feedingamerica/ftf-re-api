from django.test import TestCase
from django.test import Client
from api.models import ReportSchedule
import datetime
from datetime import date
from api.tasks import generate_report_and_save

c = Client()
responce = c.post('/api/', {
                    'run_type': 'onetime',
                    'timeframe_type' : 'monthly',
                    'report_scope' : '',
                    'report_scope_value' : '',
                    'control_type' : '',
                    'reporting_dictionary' : '',
                    'control_age_group_id' : '',
                    'date_scheduled' : '',
                    'date_custom_start' : '',
                    'date_custom_end' : '',
                    'addin_state_report' : '',
                    'addin_foodbank_report' :''})

"""
Testing functions in api/tasks.py
"""
# TODO: ensure python manage.py test api works (add self as a parameter); assertions
class TasksTesting(TestCase):
    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different timeframe types
    """
    def test_generate_report_and_save_timeframe_type():
        # constants: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), report_scope_value ("346"),
        # control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # testing all timeframe_type_id: 
        #   1: Last Month
        #   2: Rolling 12 Months
        #   3: CY To Date
        #   4: Fiscal year to date
        #   5: Custom Date Range
        for x in range(1, 6): 
            print(f"\nTesting timeframe_type_id = {x}...")

            if (x != 5):
                rs = ReportSchedule.objects.create(timeframe_type_id = x, run_type_id = 2, report_scope_id = 1, report_scope_value = "346", \
                control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today().strftime("%Y-%m-%d"))
            elif (x == 5):
                # for Custom Date Range, we need run_type_id = 1 (one time), and the date_custom_start and date_custom_end fields
                # arbitrarily choosing custom date range as 3-05-2021 to 3-15-2021
                rs = ReportSchedule.objects.create(timeframe_type_id = x, run_type_id = 1, date_custom_start = datetime.date(2021, 3, 5), \
                date_custom_end = datetime.date(2021, 3, 15), report_scope_id = 1, report_scope_value = "346", control_type_id = 1, \
                reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today().strftime("%Y-%m-%d"))
            
            generate_report_and_save(rs)

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different control types
    """
    def test_generate_report_and_save_control_type():
        # constants: report_scope_id (1; hierarchy, event, event_id), timeframe_type (1; last month), run_type_id (2; recurring),
        # report_scope_value ("346"), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # testing all control_type_id: 
        #   1: Is Grocery Service
        #   2: Prepack & Choice Only
        #   3: Produce Only
        #   4: Everything
        #   5: TEFAP
        for x in range(1, 6): 
            print(f"\nTesting control_type_id = {x}...")
            rs = ReportSchedule.objects.create(control_type_id = x, report_scope_id = 1, timeframe_type_id = 1, run_type_id = 2, \
            report_scope_value = "346", reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today().strftime("%Y-%m-%d"))
            
            generate_report_and_save(rs)

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different report scopes
    """ 
    def test_generate_report_and_save_report_scope():
        # constants: timeframe_type (2; rolling 12 months), run_type_id (2; recurring),
        # control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # below is a list of report scope values that will be used for each report scope id
        # these values were retrieved from source_beta's dim_hierarchies and dim_geos tables, to ensure that each report scope id has a 
        # value that makes sense
        # each value corresponds to a report scope id: the first value corresponds to report scope id 1, the last corresponds to report scope id 16
        # note that we are not testing report scope id 7 and 8, so their corresponding spots are empty
        scopeValList = ["1", "1", "3", "39045", "17", "21", "", "", "21", "21187", "21187970300", "40359", "21062", "18013", "3901", "2104560"]
        
        # testing all report_scope_id: 
        #   1: Hierarchy; Event; event_id
        #   2: Hierarchy; Location; loc_id
        #   3: Hierarchy; Organization; org_id
        #   4: Hierarchy; County; cnty_id
        #   5: Hierarchy; Foodbank; fb_id
        #   6: Hierarchy; State; state_id
        #   7: Hierarchy; Multi-Event; ra_id                (NOT AVAILABLE; NOT TESTED)
        #   8: Hierarchy; Multi-Location; cluster_id        (NOT AVAILABLE; NOT TESTED)
        #   9: Geography; State; fips_state
        #   10: Geography; County; fips_cnty
        #   11: Geography; Tract; fips_tract
        #   12: Geography; Zip Code Area; fips_zcta
        #   13: Geography; State Congressional District; fips_sldl
        #   14: Geography; State Senate; fips_sldu
        #   15: Geography; Federal Congressional District; fips_cd
        #   16: Geography; School District; fips_unsd
        for x in range(1, 17): 
            if (x == 7 or x == 8): 
                print(f"\nSkipping report_scope_id = {x} because it is not available.")
            else: 
                print(f"\nTesting report_scope_id = {x}...")
                rs = ReportSchedule.objects.create(report_scope_id = x, timeframe_type_id = 2, run_type_id = 2, report_scope_value = scopeValList[x - 1], \
                control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today().strftime("%Y-%m-%d"))
                
                generate_report_and_save(rs)
