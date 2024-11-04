from django.db import models
from extraorder_master.models import ExtraorderMaster
from stock.models import Stock

# Create your models here.

class ExtraorderSub(models.Model):
    extraordersub_id = models.AutoField(primary_key=True)
    #order_id = models.IntegerField()
    order=models.ForeignKey(ExtraorderMaster,to_field='order_id', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock,to_field='stock_id', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'extraorder_sub'