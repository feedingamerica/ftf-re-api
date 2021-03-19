from rest_framework import serializers
from .models import Report, ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        # fields = '__all__'
        depth = 2
        fields = ['report_schedule', 'start_date',
                  'end_date', 'date_completed']


# class ReportScheduleSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ReportSchedule
#         fields = '__all__'
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


class RunTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RunType
        fields = '__all__'


class TimeframeTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeframeType
        fields = '__all__'


class ReportScopeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportScope
        fields = '__all__'


class ControlTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ControlType
        fields = '__all__'


class ReportingDictionarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportingDictionary
        fields = '__all__'
