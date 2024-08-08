from django.db import models
from datetime import datetime
class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    get_class = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    f_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    section = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(null=True)
    fees = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'student_info'
        verbose_name = 'Student Information'
        verbose_name_plural = 'Student Information'

    def __str__(self):
        return self.name or 'No Name'
