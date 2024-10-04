from django.db import models
from student.models import Student


class LeaveRequest(models.Model):
    leave_id = models.AutoField(primary_key=True)
    # mess_id = models.IntegerField()
    mess=models.ForeignKey(Student,to_field='mess_id',on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=100)
    status = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'leave_request'