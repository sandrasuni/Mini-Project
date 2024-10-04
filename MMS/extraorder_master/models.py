from django.db import models
from student.models import Student

# Create your models here.

class ExtraorderMaster(models.Model):
    order_id = models.AutoField(db_column='order id', primary_key=True)  # Field renamed to remove unsuitable characters.
    # mess_id = models.IntegerField()
    mess=models.ForeignKey(Student,to_field='mess_id',on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    order_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'extraorder_master'