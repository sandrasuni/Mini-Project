from django.db import models
from student.models import Student

# Create your models here.

class MessBill(models.Model):
    messbill_id = models.AutoField(primary_key=True)
    billing_date = models.DateField()
    mess=models.ForeignKey(Student,to_field='mess_id',on_delete=models.CASCADE)
    mess_amount = models.DecimalField(max_digits=10, decimal_places=2)
    extra_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mess_bill'