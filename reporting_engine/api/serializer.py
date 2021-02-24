from rest_framework import serializers
from api.models import ReportSchedule

class report_schedule_serializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = ['run_type', 'timeframe_type', 'report_scope', 'report_scope_value', 'control_type', 'reporting_dictionary', 'control_age_group_id', 'date_scheduled', 'date_custom_start', 'date_custom_end', 'addin_state_report', 'addin_foodbank_report']

    def create(self, validated_data):
        """
        Create and return a new `report_schedule` instance, given the validated data.
        """
        return ReportSchedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `report_schedule` instance, given the validated data.
        """
        instance.run_type = validated_data.get('run_type', instance.run_type)
        instance.timeframe_type = validated_data.get('timeframe_type', instance.timeframe_type)
        instance.report_scope = validated_data.get('report_scope', instance.report_scope)
        instance.report_scope_value = validated_data.get('report_scope_value', instance.report_scope_value)
        instance.control_type = validated_data.get('control_type', instance.control_type)
        instance.reporting_dictionary = validated_data.get('reporting_dictionary', instance.reporting_dictionary)
        instance.control_age_group_id = validated_data.get('control_age_group_id', instance.control_age_group_id)
        instance.date_scheduled = validated_data.get('date_scheduled', instance.date_scheduled)
        instance.date_custom_start = validated_data.get('date_custom_start', instance.date_custom_start)
        instance.date_custom_end = validated_data.get('date_custom_end', instance.date_custom_end)
        instance.addin_state_report = validated_data.get('addin_state_report', instance.addin_state_report)
        instance.addin_foodbank_report = validated_data.get('addin_foodbank_report', instance.addin_foodbank_report)
        instance.save()
        return instance
