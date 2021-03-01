from rest_framework import serializers
from api.models import ReportSchedule

class ReportScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = [
                    'run_type', 
                    'timeframe_type', 
                    'report_scope', 
                    'report_scope_value', 
                    'control_type', 
                    'reporting_dictionary', 
                    'control_age_group_id', 
                    'date_scheduled', 
                    'date_custom_start', 
                    'date_custom_end', 
                    'addin_state_report', 
                    'addin_foodbank_report'
                ]
