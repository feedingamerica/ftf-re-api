from django.db import models

# Create your models here.


class Report(models.Model):
    report_name = models.CharField(max_length=255)

    def __str__(self):
        return self.report_name
