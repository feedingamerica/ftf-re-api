from django.test import TestCase
from django.test import Client
from api.models import ReportScheduler

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


# Create your tests here.
