from django.db import models

# Create your models here.


class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=10)
    type = models.CharField(max_length=45)
    uid = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'login'