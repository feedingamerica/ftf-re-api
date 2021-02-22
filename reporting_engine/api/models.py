from django.db import models

# Create your models here.


class TimeFrameType(models.Model):
    name = models.CharField(max_length=255, blank=True)
    dim_dates_reference = models.TextField(blank=True)
    current_start_date = models.DateField(null=True, blank=True)
    current_end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'time_frame_types'

    def __str__(self):
        return self.name


class ControlType(models.Model):
    name = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'control_types'

    def __str__(self):
        return self.name


class DataDefinitionType(models.Model):
    name = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'data_definition_types'

    def __str__(self):
        return self.name


class DataDefinition(models.Model):
    name = models.CharField(max_length=255, blank=True)
    definition_public = models.CharField(max_length=255, blank=True)
    calculation_notes = models.CharField(max_length=255, blank=True)
    interpretation_notes = models.CharField(max_length=255, blank=True)
    data_definition_type = models.ForeignKey(
        DataDefinitionType, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'data_definitions'

    def __str__(self):
        return self.name


class ReportScope(models.Model):
    type = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    field_reference = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'report_scopes'

    def __str__(self):
        return self.name


class ReportingDictionary(models.Model):
    name = models.CharField(max_length=255, blank=True)
    definition = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'reporting_dictionaries'

    def __str__(self):
        return self.name


class ReportingDictionarySection(models.Model):
    name = models.CharField(max_length=255, blank=True)
    reporting_dictionary = models.ForeignKey(
        ReportingDictionary, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'reporting_dictionary_sections'

    def __str__(self):
        return self.name


class ReportingDictionaryDefinition(models.Model):
    report_dictionary = models.ForeignKey(
        ReportingDictionary, on_delete=models.CASCADE, null=True, blank=True)
    data_definition = models.ForeignKey(
        DataDefinition, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(
        ReportingDictionarySection, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id', 'section_id'), )
        db_table = 'reporting_dictionary_definitions'

    def __str__(self):
        return self.name


class RunType(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'run_types'

    def __str__(self):
        return self.name


class ReportSchedule(models.Model):
    run_type = models.ForeignKey(RunType, on_delete=models.CASCADE)
    timeframe_type = models.ForeignKey(TimeFrameType, on_delete=models.CASCADE)
    report_scope = models.ForeignKey(ReportScope, on_delete=models.CASCADE)
    report_scope_value = models.CharField(max_length=255, blank=True)
    control_type = models.ForeignKey(ControlType, on_delete=models.CASCADE)
    reporting_dictionary = models.ForeignKey(
        ReportingDictionary, on_delete=models.CASCADE)
    control_age_group_id = models.IntegerField()
    date_scheduled = models.DateField()
    date_custom_start = models.DateField(null=True, blank=True)
    date_custom_end = models.DateField(null=True, blank=True)
    addin_state_report = models.ForeignKey(
        ReportingDictionary, related_name='addin_state', on_delete=models.CASCADE, null=True, blank=True)
    addin_foodbank_report = models.ForeignKey(
        ReportingDictionary, related_name='addin_foodbank', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'report_schedules'

    def __str__(self):
        return self.name


class Report(models.Model):
    report_schedule = models.ForeignKey(
        ReportSchedule, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return self.name


class AddinManager(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    reporting_dictionary = models.ForeignKey(
        ReportingDictionary, on_delete=models.CASCADE, null=True, blank=True)
    report_scope = models.ForeignKey(
        ReportScope, on_delete=models.CASCADE, null=True, blank=True)
    report_scope_value = models.PositiveIntegerField(null=True, blank=True)
    control_type = models.ForeignKey(
        ControlType, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'addin_manager'

    def __str__(self):
        return self.name


class ReportDataFloat(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, null=True, blank=True)
    data_definition = models.ForeignKey(
        DataDefinition, on_delete=models.CASCADE, null=True, blank=True)
    float_value = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'report_data_float'

    def __str__(self):
        return self.name


class ReportDataInt(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, null=True, blank=True)
    data_definition = models.ForeignKey(
        DataDefinition, on_delete=models.CASCADE, null=True, blank=True)
    int_value = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'report_data_int'

    def __str__(self):
        return self.name


class ReportDataJson(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    data_definition = models.ForeignKey(
        DataDefinition, on_delete=models.CASCADE)
    json_object = models.JSONField(blank=True)

    class Meta:
        unique_together = (('id', 'report_id', 'data_definition_id'), )
        db_table = 'report_data_json'

    def __str__(self):
        return self.name
