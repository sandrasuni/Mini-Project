from django.db import models

# Create your models here.

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=20)
    menu_item = models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True)
    menu_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'menu'