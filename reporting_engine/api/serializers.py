from .models import Report
from rest_framework import serializers


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        # fields = '__all__'
        fields = ['report_schedule', 'start_date',
                  'end_date', 'date_completed']
