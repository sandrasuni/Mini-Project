from django.db import models

# Create your models here.

class ExtraorderSub(models.Model):
    extraordersub_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    stock_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'extraorder_sub'