# leave_request/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from student.models import Student
from presence_log.models import PresenceLog
from mess_amount.models import MessAmount
from extraorder_master.models import ExtraorderMaster
from django.utils.dateparse import parse_date
from datetime import datetime
from django.db.models import Sum
from leave_request.models import LeaveRequest
from datetime import datetime


def presence(request):
    return render(request, "presence_log/presence_log.html")

def fetch_student_details(request):
    if request.method == 'GET':
        mess_id = request.GET.get('mess_id')
        try:
            # Fetch student details based on mess_id
            student = Student.objects.get(mess_id=mess_id)
            data = {
                'student_name': student.name,
                'department': student.department,
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'student_name': '', 'department': ''})  # Return empty on not found


