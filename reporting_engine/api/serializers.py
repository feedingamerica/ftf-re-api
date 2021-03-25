from rest_framework import serializers
from .models import Report, ReportSchedule, RunType, TimeframeType, ReportScope, ControlType, ReportingDictionary


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        depth = 2
        fields = ['report_schedule', 'start_date',
                  'end_date', 'date_completed']


class ReportScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = '__all__'

class RunTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunType
        fields = '__all__'


class TimeframeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeframeType
        fields = '__all__'


class ReportScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportScope
        fields = '__all__'


class ControlTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlType
        fields = '__all__'


class ReportingDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingDictionary
        fields = '__all__'
