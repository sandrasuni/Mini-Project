from django.db import models

# Create your models here.


class Student(models.Model):
    mess_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    department = models.CharField(db_column='Department', max_length=10)  # Field name made lowercase.
    joining_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'student'
