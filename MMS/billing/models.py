from django.db import models
from student.models import Student

# Create your models here.

class MessBill(models.Model):
    messbill_id = models.AutoField(primary_key=True)
    month = models.DateField()
    year = models.DateField()
    date = models.DateField()
    mess_id = models.IntegerField()
    student_name = models.CharField(max_length=45)
    mess_amount = models.IntegerField()
    extra_amount = models.IntegerField()
    total_amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mess_bill'