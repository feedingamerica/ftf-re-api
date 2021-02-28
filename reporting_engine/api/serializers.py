from .models import Report, ReportSchedule, RunType, TimeFrameType, ReportScope, ControlType, ReportingDictionary
from rest_framework import serializers


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        # fields = '__all__'
        depth = 2
        fields = ['report_schedule', 'start_date',
                  'end_date', 'date_completed']


class ReportScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = '__all__'


class RunTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RunType
        fields = '__all__'


class TimeFrameTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeFrameType
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
