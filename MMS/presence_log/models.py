from django.db import models
from student.models import Student

# Create your models here.

class PresenceLog(models.Model):
    presencelog_id = models.AutoField(primary_key=True)
    mess=models.ForeignKey(Student,to_field='mess_id',on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'presence_log'