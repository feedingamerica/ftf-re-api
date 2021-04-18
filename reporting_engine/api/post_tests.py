from django.test import Client, TestCase
from api.models import ReportSchedule
import unittest
from datetime import date

"""
Testing the django POST request for report schedules
"""
class PostTesting():
    """
    Setting up test model instances for the test database that Django creates. In order to run these 'testserver' must be added to 'ALLOWED_HOSTS' in /reporting_engine/settings.py
    Test cases will be run from the shell so begin by running "python manage.py shell", follow up with "from api.post_tests import PostTesting" and then run "PostTesting.test_call_tests()"
    If a test case passes nothing will be printed. If it fails the test case will give an Assertion Error
    """  	
    #checking for a post test success, ensuring valid input works	
    def test_post_pass(params):
        #Client and testcase initialization
        c = Client()
        tc = unittest.TestCase()
        duplicate = False
        #if the report schedule exists, set the duplicate variable to true and run the post
        if (ReportSchedule.objects.filter(run_type_id = params[0], timeframe_type_id = params[1], report_scope_id = params[2], report_scope_value = params[3], control_type_id = params[4], reporting_dictionary_id = params[5], control_age_group_id = params[6], date_scheduled = params[7]).exists()):
            duplicate = True
        #Post response
        response = c.post('/api/report_schedules/', {
                                                "run_type": params[0],
	                                            "timeframe_type": params[1],
	                                            "report_scope": params[2],
	                                            "report_scope_value": params[3],
	                                            "control_type": params[4],
	                                            "reporting_dictionary": params[5],
	                                            "control_age_group_id": params[6],
                                                "date_scheduled": params[7]
                                                }, 'application/json')

        #if the report schedule exists, ensure that status 208 is returned from the post
        if(duplicate):
            tc.assertEqual(response.status_code,208)
        #otherwise, ensure that the report schedule saves to the database and then delete the record
        else:    
            tc.assertEqual(response.status_code, 201)
            rs = ReportSchedule.objects.filter(run_type_id = params[0], timeframe_type_id = params[1], report_scope_id = params[2], report_scope_value = params[3], control_type_id = params[4], reporting_dictionary_id = params[5], control_age_group_id = params[6], date_scheduled = params[7]).get()
            tc.assertTrue(rs != None, "Report Schedule did not save to database correctly")
            rs.delete()

    #checking for a post test failure, ensuring bad input fails      
    def test_post_fail(params):
        #Client and testcase initialization
        c = Client()
        tc = unittest.TestCase()
        #Post response with assertion that value error occurs
        response = c.post('/api/report_schedules/', {
                                                "run_type": params[0],
	                                            "timeframe_type": params[1],
	                                            "report_scope": params[2],
	                                            "report_scope_value": params[3],
	                                            "control_type": params[4],
	                                            "reporting_dictionary": params[5],
	                                            "control_age_group_id": params[6],
                                                "date_scheduled": params[7]
                                                }, 'application/json')
        #ensure that the report schedule does not save to the database  
        tc.assertEqual(response.status_code, 400)
        with tc.assertRaises(ValueError):
            ReportSchedule.objects.filter(run_type_id = params[0], timeframe_type_id = params[1], report_scope_id = params[2], report_scope_value = params[3], control_type_id = params[4], reporting_dictionary_id = params[5], control_age_group_id = params[6], date_scheduled = params[7]).get()
    
    #This method calls all the test cases
    def test_call_tests():
        #checking report_scope_value only under 9 because those do not have addins      
        test1 = [2, 3, 1, 97, 1, 1, 1, date.today()]
        test2 = [2, 3, 1, 97, 1, 1, 1, date.today()]
        test3 = [2, 3, "fail", 99, 1, 1, 1, date.today()]

        PostTesting.test_post_pass(test1)
        print("Passing Post Test Successful")

        PostTesting.test_post_pass(test2)
        print("Duplicate Post Test Successful")

        PostTesting.test_post_fail(test3)
        print("Failure Post Test Successful")