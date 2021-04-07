from django.test import TestCase, Client
from api.models import ReportSchedule, ControlType, TimeframeType, RunType, ReportScope, ReportingDictionary, Report, ReportScheduleAddinReport, ReportScheduleAddin, ReportDataInt
import datetime
from datetime import date
from api.tasks import generate_report_and_save
from api.tasks import calculate_dates

"""
The tests in this file can be run using: python manage.py test api
This will run all of the tests, and Django will automatically create a test database, so nothing is added to the actual reports database
"""

"""
Testing the calculate_dates(schedule) function in api/tasks.py
"""
class TasksCalcTesting(TestCase):
    """
    Setting up test model instances for the test database that Django creates
    """
    @classmethod
    def setUpTestData(cls):
        # the tests below create a ReportSchedule object, which has several foreign keys
        # Django sets up a test database for unit testing, but it is not populated
        # so, this function creates the needed model instances so that the tests can run and refer to these models without error
        # below are ControlType, RunType, ReportScope, and ReportingDictionary test models which will be used in each test
        testCT = ControlType.objects.create(id = 1)
        testRT = RunType.objects.create(id = 2)
        testRSc = ReportScope.objects.create(id = 1)
        testRD = ReportingDictionary.objects.create(id = 1)

    """
    Testing the calculate_dates(schedule) function from tasks.py
    Testing timeframe type 1: Last Month
    """
    def test_calculate_dates_last_month(self):
        # setting up the instance TimeframeType model for this specific test
        testTfT = TimeframeType.objects.create(id = 1, name = "Last Month")
  
        # creating a schedule using the ReportSchedule model
        # parameters used to create it: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), 
        # report_scope_value (346), control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (2021-03-05)
        rs = ReportSchedule.objects.create(timeframe_type_id = 1, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
        control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=datetime.date(2021, 3, 5))

        # calling the tested function
        actual_start_date, actual_end_date = calculate_dates(rs)

        # ensuring we got expected results
        self.assertEqual(actual_start_date, datetime.date(2021, 2, 1).strftime("%Y-%m-%d"))
        self.assertEqual(actual_end_date, datetime.date(2021, 2, 28).strftime("%Y-%m-%d"))

    """
    Testing the calculate_dates(schedule) function from tasks.py
    Testing timeframe type 2: Rolling 12 Months
    """
    def test_calculate_dates_rolling(self):
        # setting up the instance TimeframeType model for this specific test
        testTfT = TimeframeType.objects.create(id = 2, name = "Rolling 12 Months")
  
        # creating a schedule using the ReportSchedule model
        # parameters used to create it: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), 
        # report_scope_value (346), control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (2021-03-05)
        rs = ReportSchedule.objects.create(timeframe_type_id = 2, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
        control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=datetime.date(2021, 3, 5))

        # calling the tested function
        actual_start_date, actual_end_date = calculate_dates(rs)

        # ensuring we got expected results
        self.assertEqual(actual_start_date, datetime.date(2020, 3, 1).strftime("%Y-%m-%d"))
        self.assertEqual(actual_end_date, datetime.date(2021, 2, 28).strftime("%Y-%m-%d"))

    """
    Testing the calculate_dates(schedule) function from tasks.py
    Testing timeframe type 3: CY To Date
    """
    def test_calculate_dates_cy(self):
        # setting up the instance TimeframeType model for this specific test
        testTfT = TimeframeType.objects.create(id = 3, name = "CY To Date")
  
        # creating a schedule using the ReportSchedule model
        # parameters used to create it: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), 
        # report_scope_value (346), control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (2021-03-05)
        rs = ReportSchedule.objects.create(timeframe_type_id = 3, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
        control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=datetime.date(2021, 3, 5))

        # calling the tested function
        actual_start_date, actual_end_date = calculate_dates(rs)

        # ensuring we got expected results
        self.assertEqual(actual_start_date, datetime.date(2021, 1, 1).strftime("%Y-%m-%d"))
        self.assertEqual(actual_end_date, datetime.date(2021, 2, 28).strftime("%Y-%m-%d"))

    """
    Testing the calculate_dates(schedule) function from tasks.py
    Testing timeframe type 4: Fiscal year to date
    """
    def test_calculate_dates_fiscal(self):
        # setting up the instance TimeframeType model for this specific test
        testTfT = TimeframeType.objects.create(id = 4, name = "Fiscal year to date")
  
        # creating a schedule using the ReportSchedule model
        # parameters used to create it: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), 
        # report_scope_value (346), control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (2021-03-05)
        rs = ReportSchedule.objects.create(timeframe_type_id = 4, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
        control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=datetime.date(2021, 3, 5))

        # calling the tested function
        actual_start_date, actual_end_date = calculate_dates(rs)

        # ensuring we got expected results
        self.assertEqual(actual_start_date, datetime.date(2020, 7, 1).strftime("%Y-%m-%d"))
        self.assertEqual(actual_end_date, datetime.date(2021, 2, 28).strftime("%Y-%m-%d"))

    """
    Testing the calculate_dates(schedule) function from tasks.py
    Testing timeframe type 5: Custom Date Range
    """
    def test_calculate_dates_custom(self):
        # setting up the instance TimeframeType model for this specific test
        testTfT = TimeframeType.objects.create(id = 5, name = "Custom Date Range")
  
        # creating a schedule using the ReportSchedule model
        # parameters used to create it: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), 
        # report_scope_value (346), control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (2021-03-05), date_custom_start (2021-02-07), date_custom_end (2021-03-04)
        rs = ReportSchedule.objects.create(timeframe_type_id = 5, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
        control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=datetime.date(2021, 3, 5), \
        date_custom_start=datetime.date(2021, 2, 7), date_custom_end=datetime.date(2021, 3, 4))

        # calling the tested function
        actual_start_date, actual_end_date = calculate_dates(rs)

        # ensuring we got expected results
        self.assertEqual(actual_start_date, datetime.date(2021, 2, 7).strftime("%Y-%m-%d"))
        self.assertEqual(actual_end_date, datetime.date(2021, 3, 4).strftime("%Y-%m-%d"))

"""
Testing the generate_report_and_save(schedule) function in api/tasks.py
"""
class TasksGenTesting(TestCase):
    """
    Setting up test model instances for the test database that Django creates
    """
    @classmethod
    def setUpTestData(cls):
        # the tests below create a ReportSchedule object, which has several foreign keys
        # Django sets up a test database for unit testing, but it is not populated
        # so, this function creates the needed model instances so that the tests can run and refer to these models without error

        # needed for all tests:
        testRT1 = RunType.objects.create(id = 1)
        testRT2 = RunType.objects.create(id = 2)

        # needed for the timeframe_type test:
        testTfT1 = TimeframeType.objects.create(id = 1, name = "Last Month")
        testTfT2 = TimeframeType.objects.create(id = 2, name = "Rolling 12 Months")
        testTfT3 = TimeframeType.objects.create(id = 3, name = "CY To Date")
        testTfT4 = TimeframeType.objects.create(id = 4, name = "Fiscal year to date")
        testTfT5 = TimeframeType.objects.create(id = 5, name = "Custom Date Range")

        # needed for the control_type test:
        testCT1 = ControlType.objects.create(id = 1, name = "Is Grocery Service")
        testCT2 = ControlType.objects.create(id = 2, name = "Prepack & Choice Only")
        testCT3 = ControlType.objects.create(id = 3, name = "Produce Only")
        testCT4 = ControlType.objects.create(id = 4, name = "Everything")
        testCT5 = ControlType.objects.create(id = 5, name = "TEFAP")

        # needed for the report_scope test:
        testRSc1 = ReportScope.objects.create(id = 1)
        testRSc2 = ReportScope.objects.create(id = 2)
        testRSc3 = ReportScope.objects.create(id = 3)
        testRSc4 = ReportScope.objects.create(id = 4)
        testRSc5 = ReportScope.objects.create(id = 5)
        testRSc6 = ReportScope.objects.create(id = 6)
        testRSc9 = ReportScope.objects.create(id = 9)
        testRSc10 = ReportScope.objects.create(id = 10)
        testRSc11 = ReportScope.objects.create(id = 11)
        testRSc12 = ReportScope.objects.create(id = 12)
        testRSc13 = ReportScope.objects.create(id = 13)
        testRSc14 = ReportScope.objects.create(id = 14)
        testRSc15 = ReportScope.objects.create(id = 15)
        testRSc16 = ReportScope.objects.create(id = 16)

        # needed for the reporting_dictionary test:
        testRD1 = ReportingDictionary.objects.create(id = 1)
        testRD2 = ReportingDictionary.objects.create(id = 2)
        testRD3 = ReportingDictionary.objects.create(id = 3)
        testRD4 = ReportingDictionary.objects.create(id = 4)
    
    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different timeframe types
    """
    def test_generate_report_and_save_timeframe_type(self):
        # constants in the report schedule: run_type_id (2; recurring), report_scope_id (1; hierarchy, event, event_id), report_scope_value (346),
        # control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # testing all timeframe_type_id: 
        #   1: Last Month
        #   2: Rolling 12 Months
        #   3: CY To Date
        #   4: Fiscal year to date
        #   5: Custom Date Range
        for x in range(1, 6): 
            # use this print statement to help debug, if needed
            # print(f"\nTesting timeframe_type_id = {x}...")

            if (x != 5):
                rs = ReportSchedule.objects.create(timeframe_type_id = x, run_type_id = 2, report_scope_id = 1, report_scope_value = 346, \
                control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today())
            elif (x == 5):
                # for Custom Date Range, we need run_type_id = 1 (one time), and the date_custom_start and date_custom_end fields
                # arbitrarily choosing custom date range as 3-05-2021 to 3-15-2021
                rs = ReportSchedule.objects.create(timeframe_type_id = x, run_type_id = 1, date_custom_start = datetime.date(2021, 3, 5), \
                date_custom_end = datetime.date(2021, 3, 15), report_scope_id = 1, report_scope_value = 346, control_type_id = 1, \
                reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today())
            
            # calling the tested function
            generate_report_and_save(rs)

            # ensuring the generated report was actually saved to the database
            self.assertTrue(Report.objects.filter(report_schedule_id = rs.pk).exists())

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different control types
    """
    def test_generate_report_and_save_control_type(self):
        # constants in the report schedule: report_scope_id (1; hierarchy, event, event_id), timeframe_type_id (2; rolling 12 months), 
        # run_type_id (2; recurring), report_scope_value (346), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # testing all control_type_id: 
        #   1: Is Grocery Service
        #   2: Prepack & Choice Only
        #   3: Produce Only
        #   4: Everything
        #   5: TEFAP
        for x in range(1, 6): 
            # use this print statement to help debug, if needed
            # print(f"\nTesting control_type_id = {x}...")

            rs = ReportSchedule.objects.create(control_type_id = x, report_scope_id = 1, timeframe_type_id = 2, run_type_id = 2, \
            report_scope_value = 346, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today())
            
            # calling the tested function
            generate_report_and_save(rs)

            # ensuring the generated report was actually saved to the database
            self.assertTrue(Report.objects.filter(report_schedule_id = rs.pk).exists())

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different report scopes
    """ 
    def test_generate_report_and_save_report_scope(self):
        # constants in the report schedule: timeframe_type_id (2; rolling 12 months), run_type_id (2; recurring),
        # control_type_id (1; Is Grocery Service), reporting_dictionary_id (1; default reporting engine output),
        # control_age_group_id (1), date_scheduled (today)

        # below is a list of report scope values that will be used for each report scope id
        # these values were retrieved from source_beta's dim_hierarchies and dim_geos tables, to ensure that each report scope id has a 
        # value that makes sense
        # each value corresponds to a report scope id: the first value corresponds to report scope id 1, the last corresponds to report scope id 16
        # note that we are not testing report scope id 7 and 8, so their corresponding spots are empty
        scopeValList = [1, 1, 3, 39045, 17, 21, "", "", 21, 21187, 21187970300, 40359, 21062, 18013, 3901, 2104560]
        
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
                # use this print statement to help debug, if needed
                # print(f"\nTesting report_scope_id = {x}...")

                rs = ReportSchedule.objects.create(report_scope_id = x, timeframe_type_id = 2, run_type_id = 2, report_scope_value = scopeValList[x - 1], \
                control_type_id = 1, reporting_dictionary_id = 1, control_age_group_id = 1, date_scheduled=date.today())
                
                # calling the tested function
                generate_report_and_save(rs)

                # ensuring the generated report was actually saved to the database
                self.assertTrue(Report.objects.filter(report_schedule_id = rs.pk).exists())

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different reporting dictionary ids
    """
    def test_generate_report_and_save_reporting_dict(self):
        # constants in the report schedule: report_scope_id (1; hierarchy, event, event_id), timeframe_type_id (2; rolling 12 months),
        # run_type_id (2; recurring), control_type_id (1; Is Grocery Service), report_scope_value (346),
        # control_age_group_id (1), date_scheduled (today)

        # testing all reporting_dictionary_id:
        #   1: Default Reporting Engine Output 
        #   2: State AddIn - Ohio
        #   3: Food Bank Add-in - MOFC
        #   4: Food Bank Add-in - Virginia Peninsula
        for x in range(1, 5): 
            # use this print statement to help debug, if needed
            # print(f"\nTesting reporting_dictionary_id = {x}...")
            
            rs = ReportSchedule.objects.create(reporting_dictionary_id = x, report_scope_id = 1, timeframe_type_id = 2, run_type_id = 2, \
            control_type_id = 1, report_scope_value = 346, control_age_group_id = 1, date_scheduled=date.today())
            
            # calling the tested function
            generate_report_and_save(rs)

            # ensuring the generated report was actually saved to the database
            self.assertTrue(Report.objects.filter(report_schedule_id = rs.pk).exists())

    """
    Testing the generate_report_and_save(schedule) function from tasks.py
    Testing generation and saving of different addin reports
    """
    def test_generate_report_and_save_addin_reports(self):
        # constants in the report schedule: report_scope_id (1; hierarchy, event, event_id), timeframe_type_id (2; rolling 12 months),
        # run_type_id (2; recurring), control_type_id (1; Is Grocery Service), report_scope_value (346),
        # control_age_group_id (1), date_scheduled (today), reporting_dictionary_id (1; default reporting engine output)

        # we are testing all addin_reports, which are types of reporting_dictionary_id:
        #   2: State AddIn - Ohio                           (here, accessed via ReportScheduleAddin primary key 1)
        #   3: Food Bank Add-in - MOFC                      (here, accessed via ReportScheduleAddin primary key 2)
        #   4: Food Bank Add-in - Virginia Peninsula        (here, accessed via ReportScheduleAddin primary key 3)
        # the addin_report is accessed through ReportScheduleAddinReport and ReportScheduleAddin; we will be inputting 
        # the primary keys of ReportScheduleAddin as our values for our ReportSchedule's addin_reports_id value
        for x in range(1, 4): 
            # use this print statement to help debug, if needed
            # print(f"\nTesting addin_reports_id = {x}...")

            # creating the necessary rows in ReportScheduleAddin
            rsa = ReportScheduleAddin.objects.create(reporting_dictionary_id = x + 1)
            
            # creating the report schedule
            rs = ReportSchedule.objects.create(report_scope_id = 1, timeframe_type_id = 2, run_type_id = 2, \
            control_type_id = 1, report_scope_value = 346, control_age_group_id = 1, date_scheduled=date.today(), reporting_dictionary_id = 1)
            
            # adding a new row to report_schedule_addin_reports which corresponds to the ReportSchedule object we just made
            # the report_schedule_addin_id refers to the ReportScheduleAddin table
            rsar = ReportScheduleAddinReport.objects.create(report_schedule_id = rs.pk, report_schedule_addin_id = x)

            # now that we have made a new ReportScheduleAddinReport object, updating our ReportSchedule object so that it 
            # has the addin_reports_id field (this field is of type ReportScheduleAddin, through ReportScheduleAddinReport)
            rs.addin_reports_id = x
            rs.save()
            
            # calling the tested function
            generate_report_and_save(rs)

            # ensuring the generated report was actually saved to the database
            self.assertTrue(Report.objects.filter(report_schedule_id = rs.pk).exists())



"""
Testing the django POST and GET request
"""
class GetPostTesting(TestCase):
    """
    Setting up test model instances for the test database that Django creates
    """
    @classmethod
    def setUpTestData(cls):
		c = Client()
  		
  	def postCleanTest(self):
        rt = 1
        tft = 2
        rs = 3
        rsv = ""
		ct = 1
        rd = 1
        cagi = 1
        ds = "2021-04-07"
		response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        response = c.post('/api/report_schedules', {"run_type": "dog",
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        self.assertTrue(response.status_code != 200)
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": "cat",
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": "fish",
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": -1,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": "snake",
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": "bird",
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": "hamster",
                                                    "date_scheduled": ds}  )
        
        self.assertEqual(response.status_code, 200)
        
        
        response = c.post('/api/report_schedules', {"run_type": rt,
                                                    "timeframe_type": tft,
                                                    "report_scope": rs,
                                                    "report_scope_value": rsv,
                                                    "control_type": ct,
                                                    "reporting_dictionary": rd,
                                                    "control_age_group_id": cagi,
                                                    "date_scheduled": "Today"}  )
        
        self.assertEqual(response.status_code, 200)



