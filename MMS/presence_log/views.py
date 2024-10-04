# leave_request/views.py
from django.shortcuts import render
from presence_log.models import PresenceLog
from datetime import datetime
from django.utils import timezone

from django.http import JsonResponse
from student.models import Student
from leave_request.models import LeaveRequest

# your_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from student.models import Student
from presence_log.models import PresenceLog

def presence(request):
    return render(request, 'presence_log/presence_log.html')

def get_student_details(request, mess_id):
    try:
        student = Student.objects.get(mess_id=mess_id)
        return JsonResponse({'name': student.name})
    except Student.DoesNotExist:
        return JsonResponse({'name': ''})

def search_presence_log(request, mess_id):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    logs = PresenceLog.objects.filter(mess_id=mess_id, date__range=[from_date, to_date])
    presence_logs = [{'date': log.date, 'mess_amount': log.mess_amount, 'extra_amount': log.extra_amount, 'status': log.status} for log in logs]
    
    return JsonResponse({'presence_logs': presence_logs})


# def get_student_details(request, mess_id):
#     try:
#         student = Student.objects.get(mess_id=mess_id)
#         leave_requests = LeaveRequest.objects.filter(mess=student, status='Approved')
        
#         if leave_requests.exists():
#             from_date = leave_requests.first().from_date
#             to_date = leave_requests.first().to_date
#             return JsonResponse({
#                 'name': student.name,
#                 'from_date': from_date.strftime('%Y-%m-%d'),
#                 'to_date': to_date.strftime('%Y-%m-%d'),
#             })
#         else:
#             return JsonResponse({'name': student.name, 'from_date': '', 'to_date': ''})

#     except Student.DoesNotExist:
#         return JsonResponse({'name': '', 'from_date': '', 'to_date': ''})

# from django.http import JsonResponse
# from student.models import Student
# from billing.models import MessBill
# from mess_amount.models import MessAmount

# def get_student_details(request, mess_id):
#     try:
#         student = Student.objects.get(mess_id=mess_id)
#         bills = Student.objects.filter(student=student)

#         bill_data = [{'date': MessBill.date, 'mess_amount': MessAmount.mess_amount, 'extra_amount': MessBill.extra_amount} for bill in bills]

#         return JsonResponse({
#             'name': student.name,
#             'bills': bill_data,
#         })

#     except Student.DoesNotExist:
#         return JsonResponse({'error': 'Student not found'}, status=404)
    

# def search_presence_log(request, mess_id):
#     from_date = request.GET.get('from_date')
#     to_date = request.GET.get('to_date')

#     logs = PresenceLog.objects.filter(
#         student__mess_id=mess_id,
#         date__range=[from_date, to_date]
#     )

#     presence_logs = [{
#         'date': log.date,
#         'mess_amount': log.mess_amount,
#         'extra_amount': log.extra_amount,
#         'status': log.status  # Can be 'Present' or 'Absent'
#     } for log in logs]

#     return JsonResponse({'presence_logs': presence_logs})


    
# def presence(request):
#     date_time = timezone.now().strftime("%Y-%m-%d")
#     if request.method == "POST":
#         mess_id = request.POST.get('mess_id')
#         student = Student.objects.get(mess_id=mess_id)
        
#         # Fetch leave details
#         leave_requests = LeaveRequest.objects.filter(mess=student, status='Approved')
        
#         for leave in leave_requests:
#             obj = PresenceLog()
#             obj.from_date = leave.from_date
#             obj.to_date = leave.to_date
#             obj.mess = student
#             obj.save()

#     context = {'dt': date_time}
#     return render(request, 'presence_log/presence_log.html', context)


# from student.models import
# import datetime


# def presence(request):
#     # dd=datetime.datetime.today()
#     date_time = timezone.now().strftime("%Y-%m-%d")
#     # ss=request.session["uid"]
#     # student_instance = Student.objects.get(pk=ss)

#     if request.method=="POST":
#         obj=PresenceLog()
#         obj.from_date = request.POST.get('from_date')
#         obj.to_date = request.POST.get('to_date')
#         # obj.mess = student_instance 
#         obj.save()
#     context={
#         'dt': date_time        
#     }  
        
#         # return redirect('view_leave')  # Redirect to the page after submitting
#     return render(request, 'presence_log/presence_log.html',context)