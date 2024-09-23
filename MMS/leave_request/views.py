# leave_request/views.py
from django.shortcuts import render
from leave_request.models import LeaveRequest
from datetime import datetime
from django.utils import timezone
from student.models import Student
# from student.models import
# import datetime
def leave(request):
    # dd=datetime.datetime.today()
    date_time = timezone.now().strftime("%Y-%m-%d")
    ss=request.session["uid"]

    if request.method=="POST":
        obj=LeaveRequest()
        obj.mess= "1"
        # obj.department = 
        obj.from_date = request.POST.get('from_date')
        # obj.from_date=datetime.datetime.today()
        obj.to_date = request.POST.get('to_date')
        obj.reason = request.POST.get('reason')
        obj.status = 'PENDING' 
        obj.save()
    context={
        'dt': date_time        
    }  
        
        # return redirect('view_leave')  # Redirect to the page after submitting
    return render(request, 'leave_request/leave_request.html',context)

def ml(request):
    obj=LeaveRequest.objects.all()
    context={
        'dd':obj
    }
    return render(request,'leave_request/manage_leave.html',context)

# Approve leave request
def approve_leave_request(request,idd):
    obj=LeaveRequest.objects.get(leave_id=idd)
    obj.status='Approved'
    obj.save()
    return ml(request)

def reject_leave_request(request,idd):
    obj=LeaveRequest.objects.get(leave_id=idd)
    obj.status='Rejected'
    obj.save()
    return ml(request)
    # return redirect('/leave_request/ml/')

def stview(request):
    obj=LeaveRequest.objects.all()
    context={
        'b':obj
    }
    return render(request,'leave_request/stview_lrequest.html',context)

def vleave(request):
    obj=LeaveRequest.objects.all()
    context={
        'dd':obj
    }
    return render(request,'leave_request/view_lrequest.html',context)