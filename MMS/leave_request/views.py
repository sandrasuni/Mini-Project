# leave_request/views.py
from django.shortcuts import render
from leave_request.models import LeaveRequest
from datetime import datetime
from django.utils import timezone
from student.models import Student
from django.db.models import Q


# def leave(request):
#     # Get the current date and time
#     date_time = timezone.now().strftime("%Y-%m-%d")
    
#     # Get leave_id from the session without error handling
#     leave_id = request.session.get("uid")

#     # Retrieve the student instance using the leave_id from the session
#     student_instance = Student.objects.get(pk=leave_id)

#     if request.method == "POST":
#         # Create a new LeaveRequest instance
#         obj = LeaveRequest()
#         obj.mess = student_instance  # Set the related student instance
#         obj.from_date = request.POST.get('from_date')
#         obj.to_date = request.POST.get('to_date')
#         obj.reason = request.POST.get('reason')
#         obj.status = 'PENDING'
#         obj.save()  # Save the new leave request to the database
    
#     # Prepare the context with the current date to display in the template
#     context = {
#         'dt': date_time
#     }
    
#     # Render the leave request form
#     return render(request, 'leave_request/leave_request.html', context)


def leave(request):
    # Get the current date
    date_time = timezone.now().strftime("%Y-%m-%d")

    # Get leave_id from the session
    leave_id = request.session.get("uid")

    # Retrieve the student instance using the leave_id from the session
    student_instance = Student.objects.get(pk=leave_id)

    if request.method == "POST":
        # Retrieve form data
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        reason = request.POST.get('reason')

        

        status_filter = Q(status='PENDING') | Q(status='Approved')
        existing_requests = LeaveRequest.objects.filter(
        mess=student_instance,
        from_date__lte=to_date,
        to_date__gte=from_date
        ).filter(status_filter)



        if existing_requests.exists():
            # If there's an existing overlapping request, render the form with an error message
            error_message = "You have already submitted a leave request for this date range."
            context = {
                'dt': date_time,
                'error_message': error_message,
                'from_date': from_date,  # Keep the entered from_date
                'to_date': to_date,      # Keep the entered to_date
                'reason': reason         # Keep the entered reason
            }
            return render(request, 'leave_request/leave_request.html', context)

        # Create a new LeaveRequest instance
        obj = LeaveRequest(
            mess=student_instance,  # Set the related student instance
            from_date=from_date,
            to_date=to_date,
            reason=reason,
            status='PENDING'
        )
        obj.save()  # Save the new leave request to the database

        # Redirect back to the leave request form without a success message
      # Assuming 'leave' is the name of the URL for this view

    # Prepare the context with the current date to display in the template
    context = {
        'dt': date_time
    }

    # Render the leave request form
    return render(request, 'leave_request/leave_request.html', context)

def ml(request):
    obj=LeaveRequest.objects.all()
    context={
        'dd':obj
    }
    return render(request,'leave_request/manage_leave.html',context)

# Approve leave request
# def approve_leave_request(request,idd):
#     obj=LeaveRequest.objects.get(leave_id=idd)
#     obj.status='Approved'
#     obj.save()
#     return ml(request)

# def reject_leave_request(request,idd):
#     obj=LeaveRequest.objects.get(leave_id=idd)
#     obj.status='Rejected'
#     obj.save()
#     return ml(request)
    # return redirect('/leave_request/ml/')

def approve_leave_request(request, idd):
    # Get the leave request object or 404 if it doesn't exist
    obj=LeaveRequest.objects.get(leave_id=idd)
    
    # Check if the request is already approved or rejected
    if obj.status == 'Pending':
        obj.status = 'Approved'
        obj.save()
    
    return ml(request)  # Redirect back to the manage leave page

# Reject leave request (Admin functionality)
def reject_leave_request(request, idd):
    # Get the leave request object or 404 if it doesn't exist
    obj=LeaveRequest.objects.get(leave_id=idd)
    
    # Check if the request is already approved or rejected
    if obj.status == 'Pending':
        obj.status = 'Rejected'
        obj.save()
    
    return ml(request)

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