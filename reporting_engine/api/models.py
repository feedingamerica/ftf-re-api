from django.db import models

# Create your models here.
class addin_manager(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    reporting_dictionary_id = models.PositiveIntegerField(null=True)
    report_scope_id = models.PositiveIntegerField(null=True)
    report_scope_value = models.PositiveIntegerField(null=True)

class control_types(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    notes = models.CharField(max_length=255,null=True)
    sql_ready_statement = models.TextField(null=True)

class data_definitions(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    definition_public = models.CharField(max_length = 255,null=True)
    calculation_notes = models.CharField(max_length = 255,null=True)
    interpretation_notes = models.CharField(max_length = 255, null=True)
    data_definition_type_id = models.CharField(max_length = 255,null=True)

class data_defintition_types(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=True)

class report_data_float(models.Model):
    id = models.IntegerField(primary_key=True)
    report_id= models.IntegerField(null=True)
    data_definition= models.IntegerField(null=True)
    float_value= models.FloatField(null=True)

class report_data_int(models.Model):
    id = models.AutoField(primary_key=True)
    report_id= models.PositiveIntegerField(null=True)
    data_definition_id= models.PositiveIntegerField(null=True)
    int_value= models.PositiveIntegerField(null=True)

class report_data_json(models.Model):
    id = models.AutoField(primary_key=True)
    report_id= models.IntegerField()
    data_definition_id= models.IntegerField()
    json_object = models.JSONField(null=True)

class Meta:
    unique_together = (('id', 'report_id', 'data_definition_id'),)

class report_schedules(models.Model):
    id = models.IntegerField(primary_key=True)
    run_type_id = models.IntegerField()
    timeframe_type_id = models.IntegerField()
    report_scope_id = models.IntegerField()
    report_scope_value = models.CharField(max_length = 255, null=True)
    control_type_id = models.IntegerField()
    reporting_dictionary_id = models.IntegerField()
    control_age_group_id = models.IntegerField()
    date_scheduled = models.DateTimeField()
    date_custom_start = models.DateTimeField(null=True)
    date_custom_end = models.DateTimeField(null=True)
    addin_state_report = models.PositiveIntegerField(null=True)
    addin_foodbank_report = models.PositiveIntegerField(null=True)

class report_scopes(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length = 255, null = True)
    name = models.CharField(max_length = 255, null = True)
    field_reference = models.CharField(max_length = 255, null = True)

class reporting_dictionaries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, null = True)
    definition = models.CharField(max_length = 255, null = True)

class reporting_dictionary_definitions(models.Model):
    id = models.IntegerField(primary_key=True)
    report_dictionary_id = models.IntegerField(null = True)
    data_definition_id = models.IntegerField(null = True)
    section_id = models.IntegerField()
	
class Meta:
    unique_together = (('id', 'section_id'),)

class reporting_dictionary_sections(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, null = True)
    reporting_dictionary_id = models.IntegerField(null = True)

class reports(models.Model):
    id = models.AutoField(primary_key=True)
    report_schedule_id = models.PositiveIntegerField() 
    run_type_id = models.IntegerField()
    timeframe_type_id = models.IntegerField()
    report_scope_id = models.IntegerField()
    report_scope_value = models.CharField(max_length= 255, null=True)
    control_type_id = models.IntegerField()
    reporting_dictionary_id = models.IntegerField()
    addin_rd_state_id = models.IntegerField(null=True)
    addin_rd_fb_id = models.IntegerField(null=True)
    control_age_group_id = models.IntegerField()
    date_sceduled = models.DateTimeField()
    date_custom_start = models.DateTimeField(null=True)
    date_custom_end = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    report_status = models.SmallIntegerField(null=True)

class run_types(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, null = True)

class timeframe_types(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255, null = True)
    dim_dates_reference = models.TextField(null = True)
    current_start_date = models.DateTimeField(null = True)
    current_end_date = models.DateTimeField(null = True)
