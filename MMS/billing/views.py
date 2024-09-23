from django.shortcuts import render
# from student.models import Student
from billing.models import MessBill
from mess_amount.models import MessAmount
from student.models import Student
from leave_request.models import LeaveRequest
from django.db.models import Q
# Create your views here.

# def vbill(request):
#     obj=MessBill.objects.all()
#     context={
#         'dd':obj
#     }
#     return render(request,'billing/billing.html',context)

# views.py

# views.py


# def mesb(request):
#     # Fetch all the mess amounts and students
#     mess_amounts = MessAmount.objects.all()
#     students = Student.objects.all()

#     # Create a context to pass data to the template
#     context = {
#         'mess_amounts': mess_amounts,
#         'students': students
#     }

#     return render(request, 'billing/billing.html', context)

from django.shortcuts import render
from billing.models import MessBill
from mess_amount.models import MessAmount
from student.models import Student
from django.utils import timezone

from django.shortcuts import render
from billing.models import MessBill
from mess_amount.models import MessAmount
from student.models import Student

def mesb(request):
    # Fetch all the mess amounts and students
    mess_amounts = MessAmount.objects.all()
    students = Student.objects.all()

    # Create a context to pass data to the template
    context = {
        'mess_amounts': mess_amounts,
        'students': students
    }

    if request.method == 'POST':
        # Assuming you want to store bills when a form is submitted
        extra = request.POST.get('extra_amount', 0)  # Get extra amount from form input, default to 0 if not provided

        for student in students:
            if mess_amounts.exists():  # Ensure there's at least one mess amount
                daily_amount = mess_amounts.first().daily_amount  # Get the first daily amount

                # Create and populate a new MessBill instance
                obk = MessBill()
                obk.month = "2024-09-23"  # Set the month
                obk.year = "2024-09-23"  # Set the year
                obk.mess_id = student.mess_id
                obk.student_name = student.name
                obk.mess_amount = daily_amount  # Use the daily amount
                obk.extra_amount = extra  # Use the extra amount
                obk.total_amount = daily_amount + int(extra)  # Calculate total amount
                obk.save()  # Save the bill to the database

        # Optionally, you can redirect to a success page or show a message
        return render(request, 'billing/billing.html', context)

    return render(request, 'billing/billing.html', context)



