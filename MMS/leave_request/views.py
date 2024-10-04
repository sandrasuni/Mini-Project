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
    student_instance = Student.objects.get(pk=ss)

    if request.method=="POST":
        obj=LeaveRequest()
        obj.mess = student_instance 
        #obj.mess= "1"
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

#def stview(request):
    # obj=LeaveRequest.objects.all()
 #   obj = LeaveRequest.objects.filter(mess=Student.mess_id)
  #  context={
   #     'b':obj
   # }
    #return render(request,'leave_request/stview_lrequest.html',context)

def stview(request):
    # Get the student's unique ID (mess_id) from the session
    student_id = request.session.get('uid')

    # Retrieve only the leave requests associated with the logged-in student
    if student_id:
        student = Student.objects.get(mess_id=student_id)
        obj = LeaveRequest.objects.filter(mess=student)  # Assuming 'mess' is a ForeignKey to Student
    else:
        obj = None  # No requests if no student is logged in

    # Pass the filtered leave requests to the template
    context = {
        'b': obj
    }
    return render(request, 'leave_request/stview_lrequest.html', context)


def vleave(request):
    obj=LeaveRequest.objects.all()
    context={
        'dd':obj
    }
    return render(request,'leave_request/view_lrequest.html',context)

def students_present(request):
    present_students_count = 0
    selected_date = None
    
    if request.method == "POST":
        selected_date = request.POST.get('date')  # Get the selected date from the form
        if selected_date:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()  # Convert to date object

            # Get all students who joined on or before the selected date
            students = Student.objects.filter(joining_date__lte=selected_date)

            # Get students on leave for the selected date
            leave_students = LeaveRequest.objects.filter(
                from_date__lte=selected_date,
                to_date__gte=selected_date,
                status='Approved'
            ).values_list('mess', flat=True)

            # Students present = Total students - Students on leave
            present_students_count = students.exclude(pk__in=leave_students).count()

    context = {
        'present_count': present_students_count if present_students_count > 0 else None,
        'selected_date': selected_date,
    }

    return render(request, 'leave_request/day_student.html', context)