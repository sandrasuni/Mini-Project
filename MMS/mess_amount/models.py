from django.db import models

# Create your models here.
class MessAmount(models.Model):
    messamount_id = models.AutoField(primary_key=True)
    daily_amount = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'mess_amount'