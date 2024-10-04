from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    item_code = models.IntegerField(unique=True)
    item_name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    threshold = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock'